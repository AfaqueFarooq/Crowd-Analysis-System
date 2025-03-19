type = ['primary', 'info', 'success', 'warning', 'danger'];

demo = {
  initPickColor: function() {
    $('.pick-class-label').click(function() {
      var new_class = $(this).attr('new-class');
      var old_class = $('#display-buttons').attr('data-class');
      var display_div = $('#display-buttons');
      if (display_div.length) {
        var display_buttons = display_div.find('.btn');
        display_buttons.removeClass(old_class);
        display_buttons.addClass(new_class);
        display_div.attr('data-class', new_class);
      }
    });
  },

  initDocChart: function() {
    chartColor = "#FFFFFF";

    // General configuration for the charts with Line gradientStroke
    gradientChartOptionsConfiguration = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      tooltips: {
        bodySpacing: 4,
        mode: "nearest",
        intersect: 0,
        position: "nearest",
        xPadding: 10,
        yPadding: 10,
        caretPadding: 10
      },
      responsive: true,
      scales: {
        yAxes: [{
          display: 0,
          gridLines: 0,
          ticks: {
            display: false
          },
          gridLines: {
            zeroLineColor: "transparent",
            drawTicks: false,
            display: false,
            drawBorder: false
          }
        }],
        xAxes: [{
          display: 0,
          gridLines: 0,
          ticks: {
            display: false
          },
          gridLines: {
            zeroLineColor: "transparent",
            drawTicks: false,
            display: false,
            drawBorder: false
          }
        }]
      },
      layout: {
        padding: {
          left: 0,
          right: 0,
          top: 15,
          bottom: 15
        }
      }
    };
  },

  initDashboardPageCharts: function(chart_labels, chart_data) {


    gradientBarChartConfiguration = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },

      tooltips: {
        backgroundColor: '#f5f5f5',
        titleFontColor: '#333',
        bodyFontColor: '#666',
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest"
      },
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        yAxes: [{

          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            beginAtZero: true,
            suggestedMin: 5,
            suggestedMax: 40,
            padding: 20,
            fontColor: "#9e9e9e"
          }
        }],

        xAxes: [{

          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 5,
            fontColor: "#9e9e9e"
          }
        }]
      }
    };

    
    var ctx = document.getElementById("chartBig1").getContext('2d');
    var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
    gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
    gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors


    var myChart = new Chart(ctx, {
      type: 'line',
      responsive: true,
      legend: {
        display: true
      },
      data: {
        labels: chart_labels,
        datasets: [{
          label: "People Count",
          fill: true,
          backgroundColor: gradientStroke,
          hoverBackgroundColor: gradientStroke,
          borderColor: '#1f8ef1',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          data: chart_data,
        }]
      },
      options: gradientBarChartConfiguration
    });
    $("#0").click(function() {
      var data = myChart.config.data;
      data.datasets[0].data = chart_data;
      data.labels = chart_labels;
      myChart.update();
    });

    var ctx = document.getElementById("chartBig2").getContext('2d');
    var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
    gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
    gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors


    var myChart2 = new Chart(ctx, {
      type: 'bar',
      responsive: true,
      legend: {
        display: true
      },
      data: {
        labels: chart_labels,
        datasets: [{
          label: "Occupation",
          fill: true,
          backgroundColor: gradientStroke,
          hoverBackgroundColor: gradientStroke,
          borderColor: '#1f8ef1',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          data: chart_data,
        }]
      },
      options: gradientBarChartConfiguration
    });
    $("#0").click(function() {
      var data = myChart2.config.data;
      data.datasets[0].data = chart_data;
      data.labels = chart_labels;
      myChart2.update();
    });
  },


  
  // initDashboardPageCharts1: function(chart_gdata, chart_glabels) {


  //   gradientBarChartConfiguration2 = {
  //     maintainAspectRatio: false,
  //     legend: {
  //       display: false
  //     },

  //     tooltips: {
  //       backgroundColor: '#f5f5f5',
  //       titleFontColor: '#333',
  //       bodyFontColor: '#666',
  //       bodySpacing: 4,
  //       xPadding: 12,
  //       mode: "nearest",
  //       intersect: 0,
  //       position: "nearest"
  //     },
  //     responsive: true,
  //     maintainAspectRatio: false,
  //     scales: {
  //       yAxes: [{

  //         gridLines: {
  //           drawBorder: false,
  //           color: 'rgba(29,140,248,0.1)',
  //           zeroLineColor: "transparent",
  //         },
  //         ticks: {
  //           beginAtZero: true,
  //           suggestedMin: 5,
  //           suggestedMax: 25,
  //           padding: 20,
  //           fontColor: "#9e9e9e"
  //         }
  //       }],

  //       xAxes: [{

  //         gridLines: {
  //           drawBorder: false,
  //           color: 'rgba(29,140,248,0.1)',
  //           zeroLineColor: "transparent",
  //         },
  //         ticks: {
  //           padding: 5,
  //           fontColor: "#9e9e9e"
  //         }
  //       }]
  //     }
  //   };

  //   // var chart_labels = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
  //   // var chart_data = [100, 70, 90, 70, 85, 60, 75, 60, 90, 80, 110, 100];
    
  //   var ctx = document.getElementById("chartBig1").getContext('2d');
  //   var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

  //   gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
  //   gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
  //   gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors


  //   var myChart2 = new Chart(ctx, {
  //     type: 'bar',
  //     responsive: true,
  //     legend: {
  //       display: true
  //     },
  //     data: {
  //       labels: chart_glabels,
  //       datasets: [{
  //         label: "Gender Classify",
  //         fill: true,
  //         backgroundColor: gradientStroke,
  //         hoverBackgroundColor: gradientStroke,
  //         borderColor: '#1f8ef1',
  //         borderWidth: 2,
  //         borderDash: [],
  //         borderDashOffset: 0.0,
  //         data: chart_gdata,
  //       }]
  //     },
  //     options: gradientBarChartConfiguration2
  //   });
  //   $("#0").click(function() {
  //     var data = myChart2.config.data;
  //     data.datasets[0].data = chart_gdata;
  //     data.labels = chart_glabels;
  //     myChart2.update();
  //   });
  // },

};