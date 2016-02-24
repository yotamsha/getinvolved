/**
 * Created by yotam on 13/2/2016.
 */
angular.module('app.common.constants', [])

    .constant('AUTH_EVENTS', {
        notAuthenticated: 'auth-not-authenticated',
        notAuthorized: 'auth-not-authorized',
        authenticationCompleted: 'auth-completed',
    })

    .constant('USER_ROLES', {
        admin: 'admin_role',
        user: 'user_role',
        public: 'public_role'
    })
    .constant('TASK_STATES', {
        TASK_UNDEFINED: '__undefined__',
        TASK_PENDING: 'pending',
        TASK_ASSIGNMENT_IN_PROCESS: 'assignment_in_process',
        TASK_PENDING_USER_APPROVAL: 'pending_user_approval',
        TASK_ASSIGNED: 'assigned',
        TASK_CANCELLED: 'cancelled',
        TASK_COMPLETED: 'completed'
    });
