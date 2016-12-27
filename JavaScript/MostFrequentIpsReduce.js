/**
 * Created by Alexander on 12/27/2016.
 */

function (key, values) {
    var sum = 0;
    values.forEach(function (val) {
        sum += val['count'];
    });
    return {count: NumberInt(sum)};
}