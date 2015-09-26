/**
 * Created by Bar Wachtel on 26/09/2015.
 */
exports.getUser = function(req, res, next) {
    res.json({
        success: true,
        user: req.user
    });
}