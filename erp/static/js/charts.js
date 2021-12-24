// Chart Campaign - ApexCharts
var options = {
    chart: {
        type: 'line'
    },
    stroke: {
        width: 2,
        colors: ['#cc3333']
    },
    markers: {
        size: 0,
        colors: ['#cc3333']
    },
    series: [{
        name: 'Campaigns',
        data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }],
    xaxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },
    yaxis: [{
            axisTicks: {
                show: true
            },
            title: {
                text: "SMS CAMPAIGNS",
            }
        },

    ],
}

var Campaignchart = new ApexCharts(document.querySelector("#Campaignchart"), options);

Campaignchart.render();


// Chart Campaign - ApexCharts
var options = {
    chart: {
        type: 'line'
    },
    stroke: {
        width: 2,
        colors: ['#cc3333']
    },
    markers: {
        size: 0,
        colors: ['#cc3333']
    },
    series: [{
        name: 'Customers',
        data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }],
    xaxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },
    yaxis: [{
        axisTicks: {
            show: true
        },
        title: {
            text: "EMAIL CAMPAIGNS"
        }
    }, ],
}

var Customerschart = new ApexCharts(document.querySelector("#Customerschart"), options);

Customerschart.render();