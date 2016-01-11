FORMAT: 1A
HOST: http://example.com/api

# gi-server
a Sails application


# Group Tasks

## Tasks Collection [/task]

### List All Tasks [GET]

+ Response 200 (application/json; charset=utf-8)
    + Attributes (array[task])

+ Response 404


+ Response 500


### Create Task [POST]

+ Request

        {
            "name" : "Tom",
            "city" : "TLV"
        }

+ Response 201 (application/json; charset=utf-8)
    + Attributes (task)

+ Response 404


+ Response 500


## Task [/task/{id}]

+ Parameters
    + id (required,`1`)


### Retrieve Task By Id [GET]

+ Response 200 (application/json; charset=utf-8)
    + Attributes (task)

+ Response 404


+ Response 500


### Update Task By Id [PUT]

+ Response 200 (application/json; charset=utf-8)
    + Attributes (task)

+ Response 404


+ Response 500






## User Tasks By Parentid And Id [/user/{parentid}/tasks/{id}]

+ Parameters
    + parentid (required,`1`)

    + id (required,`1`)


### UserTasksByParentidAndId [GET]

+ Response 200 (application/json; charset=utf-8)
    + Attributes (array[task])

+ Response 404


+ Response 500


# Group Users

## Task Participants By Parentid And Id [/task/{parentid}/participants/{id}]

+ Parameters
    + parentid (required,`1`)

    + id (required,`1`)


### TaskParticipantsByParentidAndId [GET]

+ Response 200 (application/json; charset=utf-8)
    + Attributes (array[user])

+ Response 404


+ Response 500



## User By Id [/user/{id}]

+ Parameters
    + id (required,`1`)


### UserById [GET]

+ Response 200 (application/json; charset=utf-8)
    + Attributes (user)

+ Response 404


+ Response 500


### UserById [PUT]

+ Response 200 (application/json; charset=utf-8)
    + Attributes (user)

+ Response 404


+ Response 500


### UserById [POST]

+ Response 200 (application/json; charset=utf-8)
    + Attributes (user)

+ Response 404


+ Response 500



## User [/user]

### User [GET]

+ Response 200 (application/json; charset=utf-8)
    + Attributes (array[user])

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

