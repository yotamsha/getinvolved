FORMAT: 1A
HOST: http://example.com/api

# gi-server
a Sails application

# Group Swagger

## Swagger Doc [/swagger/doc]

### SwaggerDoc [GET]

+ Response 404


+ Response 500


### SwaggerDoc [PUT]

+ Response 404


+ Response 500


### SwaggerDoc [POST]

+ Response 404


+ Response 500


### SwaggerDoc [DELETE]

+ Response 404


+ Response 500


### SwaggerDoc [PATCH]

+ Response 404


+ Response 500




# Group Task

## Task By Id [/task/{id}]

+ Parameters
    + id (string, required)


### TaskById [GET]

+ Response 200 (application/json)
    + Attributes (task)

+ Response 404


+ Response 500


### TaskById [PUT]

+ Response 200 (application/json)
    + Attributes (task)

+ Response 404


+ Response 500


### TaskById [POST]

+ Response 200 (application/json)
    + Attributes (task)

+ Response 404


+ Response 500



## User Tasks By Parentid And Id [/user/{parentid}/tasks/{id}]

+ Parameters
    + parentid (string, required)

    + id (string, required)


### UserTasksByParentidAndId [GET]

+ Response 200 (application/json)
    + Attributes (task)

+ Response 404


+ Response 500


### UserTasksByParentidAndId [POST]

+ Response 200 (application/json)
    + Attributes (task)

+ Response 404


+ Response 500


### UserTasksByParentidAndId [DELETE]

+ Response 200 (application/json)
    + Attributes (task)

+ Response 404


+ Response 500



## Task [/task]

### Task [GET]

+ Response 200 (application/json)
    + Attributes (task)

+ Response 404


+ Response 500


### Task [POST]

+ Response 200 (application/json)
    + Attributes (task)

+ Response 404


+ Response 500




# Group User

## Task Participants By Parentid And Id [/task/{parentid}/participants/{id}]

+ Parameters
    + parentid (string, required)

    + id (string, required)


### TaskParticipantsByParentidAndId [GET]

+ Response 200 (application/json)
    + Attributes (user)

+ Response 404


+ Response 500


### TaskParticipantsByParentidAndId [POST]

+ Response 200 (application/json)
    + Attributes (user)

+ Response 404


+ Response 500


### TaskParticipantsByParentidAndId [DELETE]

+ Response 200 (application/json)
    + Attributes (user)

+ Response 404


+ Response 500



## User By Id [/user/{id}]

+ Parameters
    + id (string, required)


### UserById [GET]

+ Response 200 (application/json)
    + Attributes (user)

+ Response 404


+ Response 500


### UserById [PUT]

+ Response 200 (application/json)
    + Attributes (user)

+ Response 404


+ Response 500


### UserById [POST]

+ Response 200 (application/json)
    + Attributes (user)

+ Response 404


+ Response 500



## User [/user]

### User [GET]

+ Response 200 (application/json)
    + Attributes (user)

+ Response 404


+ Response 500


### User [POST]

+ Response 200 (application/json)
    + Attributes (user)

+ Response 404


+ Response 500



## User [/user/]

### User [POST]

+ Response 200 (application/json)
    + Attributes (user)

+ Response 404


+ Response 500



## User Login [/user/login]

### UserLogin [POST]

+ Response 200 (application/json)
    + Attributes (user)

+ Response 404


+ Response 500




# Unnammed Endpoint [/]

## Unnammed Endpoint [GET]

+ Response 404


+ Response 500



# Login [/login]

## Login [GET]

+ Response 404


+ Response 500


## Login [POST]

+ Response 404


+ Response 500



# Signup [/signup]

## Signup [GET]

+ Response 404


+ Response 500



# Tasks Create [/tasks/create]

## TasksCreate [GET]

+ Response 404


+ Response 500



# Group Auth

## Logout [/logout]

### Logout [POST]

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
+ `createdAt` (string, optional)
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


## contact_contacts_contact__group_contacts (object)


### Properties
+ `id` (number, optional)
+ `group_contacts` (string, optional)
+ `contact_contacts_contact` (string, optional)


## task_participants__user_tasks (object)


### Properties
+ `id` (number, optional)
+ `task_participants` (string, optional)
+ `user_tasks` (string, optional)

