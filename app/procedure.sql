use tastemaker;
DELIMITER //
CREATE PROCEDURE Result(
    IN flag VARCHAR(255)
)
BEGIN
        DECLARE done BOOLEAN DEFAULT FALSE;
        DECLARE recipeId VARCHAR(10);
        DECLARE num_steps VARCHAR(50);
        DECLARE recipeName VARCHAR(100);
        DECLARE difficulty VARCHAR(20);
        DECLARE recipe_cur CURSOR FOR 
            (SELECT r.recipe_id, r.name, r.num_steps FROM Recipe r
            WHERE r.recipe_id IN (SELECT recipe_id FROM Review GROUP BY recipe_id HAVING AVG(rating) > 3));
            
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    IF (flag = 'difficulty') THEN
        DROP TABLE IF EXISTS NewTable; 
        
        CREATE TABLE NewTable(recipe_id VARCHAR(10), name VARCHAR(100), difficulty VARCHAR(50), PRIMARY KEY(recipe_id));
        
        OPEN recipe_cur;
        REPEAT
                FETCH recipe_cur INTO recipeId, recipeName, num_steps;

                IF (num_steps > 8) THEN
                    SET difficulty = "Difficult";
                ELSEIF (num_steps  <= 8) AND (num_steps > 5) THEN
                    SET difficulty = "Medium";
                ELSE
                    SET difficulty = "Easy";
                END IF;
                
                INSERT IGNORE INTO NewTable
                VALUES (recipeId, recipeName, difficulty);
        UNTIL done
        END REPEAT;

        CLOSE recipe_cur;

        SELECT * FROM NewTable LIMIT 15;
    ELSEIF (flag = 'healthy') THEN
        (SELECT r.recipe_id, r.name, r.calories as Calories
            FROM Recipe r JOIN RecipeHasTags rt ON r.recipe_id = rt.recipe_id
            WHERE rt.tag_name = 'healthy' OR rt.tag_name = 'very-low-carbs' AND r.recipe_id IN (SELECT recipe_id FROM Review GROUP BY recipe_id HAVING COUNT(rating) > 4)
            GROUP BY r.recipe_id)
            UNION
            (SELECT r.recipe_id, r.name, r.calories as Calories
            FROM Recipe r JOIN RecipeHasTags rt ON r.recipe_id = rt.recipe_id
            WHERE r.sugar < 50 AND rt.tag_name = 'desserts' AND r.recipe_id IN (SELECT recipe_id FROM Review GROUP BY recipe_id HAVING AVG(rating) > 2))
            LIMIT 15;
    ELSEIF (flag = 'swathi') THEN
        SELECT r.recipe_id, r.name, COUNT(ingredient_id) as num_ingredients
                FROM RecipeHasIngredients rhi natural join Recipe r
                WHERE r.name LIKE '5 minute%%' AND rhi.recipe_id IN (SELECT recipe_id FROM Review GROUP BY recipe_id HAVING avg(rating) > 3)
                GROUP BY r.recipe_id, r.name
                HAVING num_ingredients < 8
                ORDER BY num_ingredients ASC, r.name ASC
                LIMIT 15;
    END IF;
END //
DELIMITER ;

