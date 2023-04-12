## Endpoints tree
- /login
- /professor/
    - /classes
    - /exercises
    - /metrics
    - /exercises/{id}/ranking
    - /exercises/{id}/students/{id}
- /student
    - /exercises/{id}
    - /exercises/{id}/solution

  
### For professors and students:
POST             /login

https://mep-org.github.io/Prototype/#/professor/publicExercises
+ https://mep-org.github.io/Prototype/#/student/publicExercises
GET              /public_exercises?filter1=...&filter2=...&page={pg}
-----> List<ExercisePreview> + List<Professor_name_id> + pagination stuff

### For professors:
https://mep-org.github.io/Prototype/#/professor/classes:
  - GET/POST         /professors/888/classes -----> List<ClassPreview>

https://mep-org.github.io/Prototype/#/professor/classes/1
  - GET/PUT/DELETE   /professors/888/classes/3 -----> Class

https://mep-org.github.io/Prototype/#/professor/exercises
+ https://mep-org.github.io/Prototype/#/professor/exercises/add
  - GET/POST         /professors/888/exercises -----> List<ExercisePreview> + List<Class_name_id>

https://mep-org.github.io/Prototype/#/professor/exercises/1
  - GET/PUT/DELETE   /professors/888/exercises/3 -----> Exercise + List<Class_name_id> + List<Metric_name_id> + [includes ranking]
  - GET              /professors/888/exercises/3/solutions/102534 (standby)

https://mep-org.github.io/Prototype/#/professor/metrics
  - GET/POST         /professors/888/metrics -----> List<Other_Metrics> + List<My_Metrics>

(URL em standby)https://mep-org.github.io/Prototype/#/professor/metrics/1
  - GET/PUT/DELETE  /professors/888/metrics/3

### For students:
https://mep-org.github.io/Prototype/#/student/home
  - GET              /students/102534/classes -----> List<ClassPreview>
  - GET              /students/102534/stats -----> Student_#doneExs_#currentExs_#nextEx_#rankLastEx

https://mep-org.github.io/Prototype/#/student/ViewClass:
https://mep-org.github.io/Prototype/#/professor/classes/1
  - GET   /students/102534/classes/3 -----> Class

https://mep-org.github.io/Prototype/#/student/assignments
  - GET              /students/102534/assignments -----> List<ExercisePreview>

https://mep-org.github.io/Prototype/#/student/assignments/1
  - GET/PUT/DELETE   /students/102534/assignments/3 -----> Exercise + [includes ranking]
  - GET              /students/102534/assignments/3/solution
