## For professors and students:
POST             /login

https://mep-org.github.io/Prototype/#/professor/publicExercises
+ https://mep-org.github.io/Prototype/#/student/publicExercises
  - GET              /public_exercises?filter1=...&filter2=...&page={pg} -----> List<ExercisePreview> + List<Professor_name_id> + pagination stuff


## For professors:
https://mep-org.github.io/Prototype/#/professor/classes:
  - GET         /professors/888/classes -----> List<ClassPreview>
  - POST        /professors/888/classes        {Class with image link}

https://mep-org.github.io/Prototype/#/professor/classes/1
  - GET          /professors/888/classes/3 -----> Class
  - PUT/DELETE   /professors/888/classes/3     {Class with image link}

https://mep-org.github.io/Prototype/#/professor/exercises
+ https://mep-org.github.io/Prototype/#/professor/exercises/add
  - GET         /professors/888/exercises -----> List<ExercisePreview> + List<Class_name_id>
  - POST        /professors/888/exercises        {Exercise with links for datasets}

https://mep-org.github.io/Prototype/#/professor/exercises/1
  - GET              /professors/888/exercises/3 -----> Exercise + List<Class_name_id> + List<Metric_name_id> + [includes ranking]
  - PUT/DELETE       /professors/888/exercises/3     {Exercise with links for datasets}
  - GET              /professors/888/exercises/3/solutions/102534 (not supported in the prototype) -----> link to solution.py

https://mep-org.github.io/Prototype/#/professor/metrics
  - GET              /professors/888/metrics -----> List<Other_Metrics> + List<My_Metrics>

(Future URL) https://mep-org.github.io/Prototype/#/professor/metrics/1
  - GET              /professors/888/metrics/3 -----> Metric
  - PUT/DELETE       /professors/888/metrics/3     {Metric}


### For students:
https://mep-org.github.io/Prototype/#/student/home
  - GET              /students/102534/classes -----> List<ClassPreview>
  - GET              /students/102534/stats -----> Student_#doneExs_#currentExs_#nextEx_#rankLastEx

https://mep-org.github.io/Prototype/#/student/ViewClass:
https://mep-org.github.io/Prototype/#/professor/classes/1
  - GET              /students/102534/classes/3 -----> Class

https://mep-org.github.io/Prototype/#/student/assignments
  - GET              /students/102534/assignments -----> List<ExercisePreview>

https://mep-org.github.io/Prototype/#/student/assignments/1
  - GET              /students/102534/assignments/3 -----> Exercise (includes links for train.csv and test.csv without Y) + [includes ranking]
  - POST             /students/102534/assignments/3    {solution.py, results.csv}


Files for /media:
- Class image
- Professor -> train.csv, test.csv (divide in X and Y)
- Student -> results.csv, solution.py
- metric.py (to run in the server)