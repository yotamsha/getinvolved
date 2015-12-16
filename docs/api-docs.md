

# Group Task

## Task [/task/{id}]
  + Parameters
    + id (required, `2`)


### Retrieve Task By Id [GET]

  + Response 200 (application/json; charset=utf-8)
  + Attributes (task)

  + Response 404


  + Response 500

### Update Task By Id [GET]

  + Response 200 (application/json; charset=utf-8)
    + Attributes (task)

  + Response 404


  + Response 500



# Data Structures

## contact (object)


### Properties
  + `group` (string, optional)
  + `id` (number, optional)
  + `createdAt` (string, optional)
  + `updatedAt` (string, optional)


## group (object)


### Properties
  + `id` (number, optional)
  + `createdAt` (string, optional)
  + `updatedAt` (string, optional)


## task (object)


### Properties
  + `name` (string, optional)
  + `createdAt` (number, optional)
  + `city` (string, optional)
  + `immediate` (boolean, optional)
  + `id` (number, optional)
  + `updatedAt` (string, optional)
  + `participants` (array, optional)


## user (object)


### Properties
  + `email` (string, optional)
  + `username` (string, optional)
  + `password` (string, optional)
  + `accessToken` (string, optional)
  + `firstName` (string, optional)
  + `lastName` (string, optional)
  + `socialNetworkId` (number, optional)
  + `socialId` (string, optional)
  + `socialAccessToken` (string, optional)
  + `isAdmin` (boolean, optional)
  + `id` (number, optional)
  + `createdAt` (string, optional)
  + `updatedAt` (string, optional)


## volunteeringapplication (object)


### Properties
  + `firstName` (string, optional)
  + `lastName` (string, optional)
  + `email` (string, optional)
  + `phoneNumber` (string, optional)
  + `volunteerArea` (string, optional)
  + `volunteerDate` (string, optional)
  + `sex` (string, optional)
  + `id` (number, optional)
  + `createdAt` (string, optional)
  + `updatedAt` (string, optional)



## task_participants__user_tasks (object)


### Properties
  + `id` (number, optional)
  + `task_participants` (string, optional)
  + `user_tasks` (string, optional)

