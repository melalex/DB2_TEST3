/**
 * Created by Alexander on 12/27/2016.
 */

function () {
    var key = { Ip: this.Ip };
    emit(key, { count: 1});
}