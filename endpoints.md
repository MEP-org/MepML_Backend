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
login
GET              /public_exercises

### For professors:
GET/POST         /professors/888/classes
GET/PUT/DELETE   /professors/888/classes/3
GET/POST         /professors/888/exercises
GET/PUT/DELETE   /professors/888/exercises/3                    [includes ranking]
GET              /professors/888/exercises/3/solutions/102534
GET/POST         /professors/888/metrics
GET/POST/DELETE  /professors/888/metrics/3

### For students:
GET/POST         /students/102534/assignments
GET/PUT/DELETE   /students/102534/assignments/3                 [includes ranking]