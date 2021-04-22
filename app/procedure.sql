use tastemaker;
DELIMITER //
CREATE PROCEDURE Result()
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

    SET @q2 = (SELECT r.recipe_id, COUNT(ingredient_id) as num_ingredients
    FROM RecipeHasIngredients rhi natural join Recipe r
    WHERE rhi.recipe_id IN (SELECT recipe_id FROM Review GROUP BY recipe_id
    HAVING avg(rating) > 3)
    GROUP BY r.name);
    
    SET @q3 = (SELECT r.recipe_id, r.minutes
    FROM Recipe r
    WHERE r.recipe_id IN (SELECT recipe_id FROM Review GROUP BY recipe_id HAVING AVG(rating) > 3));

	SELECT r.recipe_id, r.name, r.difficulty, q2.num_ingredients, q3.minutes 
    FROM NewTable r NATURAL JOIN q2 
    NATURAL JOIN q3;
END //
DELIMITER ;

