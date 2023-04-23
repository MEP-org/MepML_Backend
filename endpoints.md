## For professors and students:
POST             /login

https://mep-org.github.io/Prototype/#/professor/publicExercises
+ https://mep-org.github.io/Prototype/#/student/publicExercises
  - [DONE] GET              /public_exercises?filter1=...&filter2=...&page={pg} -----> List<ExercisePreview> + List<Professor_name_id> + pagination stuff


## For professors:
https://mep-org.github.io/Prototype/#/professor/classes:
  - [DONE] GET         /professors/888/classes -----> List<ClassPreview>
  - [DONE] POST        /professors/888/classes        {Class}

https://mep-org.github.io/Prototype/#/professor/classes/1
  - [add +details for students list] GET          /professors/888/classes/3 -----> Class with List<Student_name_id>
  - [DONE]                           PUT/DELETE   /professors/888/classes/3        {Class}
  - _                                POST         /professors/888/classes/3/students -----> List<Student_id>

https://mep-org.github.io/Prototype/#/professor/exercises
+ https://mep-org.github.io/Prototype/#/professor/exercises/add
  - [DONE] GET         /professors/888/exercises -----> List<ExercisePreview> + List<Class_name_id>
  - [DONE] POST        /professors/888/exercises        {Exercise}

https://mep-org.github.io/Prototype/#/professor/exercises/1
  - [MUST BE TESTED] GET              /professors/888/exercises/3 -----> Exercise + List<Class_name_id> + List<Metric_name_id> + List<Result>
  - [DONE]           PUT/DELETE       /professors/888/exercises/3     {Exercise}
  - GET              /professors/888/exercises/3/solutions (not supported in the prototype) -----> link to solution.py

https://mep-org.github.io/Prototype/#/professor/metrics
  - [DONE] GET              /professors/888/metrics -----> List<Other_Metrics_Preview> + List<My_Metrics_Preview>
  - [DONE] POST             /professors/888/metrics        {Metric}

(Future URL) https://mep-org.github.io/Prototype/#/professor/metrics/1
  - [DONE] GET              /professors/888/metrics/3 -----> Metric
  - [DONE] PUT/DELETE       /professors/888/metrics/3     {Metric}


### For students:
https://mep-org.github.io/Prototype/#/student/home
- GET              /students/102534/classes -----> List<ClassPreview>
- GET              /students/102534/stats -----> Student_#doneExs_#currentExs_#nextEx_#rankLastEx

https://mep-org.github.io/Prototype/#/student/ViewClass:
https://mep-org.github.io/Prototype/#/professor/classes/1
  - GET              /students/102534/classes/3 -----> Class

https://mep-org.github.io/Prototype/#/student/assignments
- [DONE] GET              /student/102534/assignments -----> List<ExercisePreview>

https://mep-org.github.io/Prototype/#/student/assignments/1
  - GET              /students/102534/assignments/3 -----> Exercise + [includes ranking]
  - POST             /students/102534/assignments/3    {solution.py, results.csv}


Files for /media:
- Class image
- Professor -> train.csv, test.csv (divide in X and Y)
- Student -> results.csv, solution.py
- metric.py (to run in the server)