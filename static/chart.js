var xValues = {{protocalNames}};
var yValues = {{sum_FIN}};
var barColors = ["#FF5733",
"#FFC300",
"#C70039",
"#900C3F",
"#581845",
"#2E86C1",
"#138D75",
"#F1C40F",
"#9B59B6",
"#CB4335"];

new Chart("myChart", {
  type: "bar",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {
    legend: {display: false},
    title: {
      display: true,
      text: "TOP 10 protocols having avg(initial window)"
    }
  }
});
