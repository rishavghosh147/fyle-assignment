-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

WITH MaxGradedAssignments AS (
    SELECT teacher_id
    FROM Assignments
    GROUP BY teacher_id
    ORDER BY COUNT(*) DESC
    LIMIT 1
)
SELECT COUNT(*) AS grade_A_count
FROM Assignments
WHERE grade = 'A' AND teacher_id = (SELECT teacher_id FROM MaxGradedAssignments);