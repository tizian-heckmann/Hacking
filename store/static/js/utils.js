/**
 * This function is directly copied from the official flask-jwt-extended documentation:
 * https://flask-jwt-extended.readthedocs.io/en/stable/token_locations.html#cookies
 *
 * Get the value of the cookie with the corresponding name. Undefined if name is not found.
 * @param {string} name - the key to get the value of inside the cookie
 * @returns the value of the cookie
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(";").shift();
    }
}
