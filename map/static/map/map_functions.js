
function draw_ce_trajectory(license, index) {
    console.log('Getting ce trajectory, license and index is:', license, index)
    $.ajax({
        url: "{% url 'map:ce_trajectory' %}",
        data:{}
    })
}