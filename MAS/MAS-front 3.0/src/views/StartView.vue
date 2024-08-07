<template>
    <div id="main" style="width: 100%; height: 100vh;"></div>
  </template>
  
  <script>
  import * as echarts from 'echarts';
  
  export default {
    name: 'StartView',
    mounted() {
      this.initChart();
      setTimeout(() => {
        this.$router.push({ name: 'CaseSelect' });
      }, 3000);
    },
    methods: {
      initChart() {
        const chartDom = document.getElementById('main');
        const myChart = echarts.init(chartDom);
        const option = {
          graphic: {
            elements: [
              {
                type: 'text',
                left: 'center',
                top: 'center',
                style: {
                  text: 'MAS',
                  fontSize: 80,
                  fontWeight: 'bold',
                  lineDash: [0, 200],
                  lineDashOffset: 0,
                  fill: 'transparent',
                  stroke: '#000',
                  lineWidth: 1,
                },
                keyframeAnimation: {
                  duration: 3000,
                  loop: true,
                  keyframes: [
                    {
                      percent: 0.7,
                      style: {
                        fill: 'transparent',
                        lineDashOffset: 200,
                        lineDash: [200, 0],
                      },
                    },
                    {
                      // Stop for a while.
                      percent: 0.8,
                      style: {
                        fill: 'transparent',
                      },
                    },
                    {
                      percent: 1,
                      style: {
                        fill: 'rgb(126,12,100)',
                      },
                    },
                  ],
                },
              },
            ],
          },
        };
        option && myChart.setOption(option);
      },
    },
  };
  </script>
  
  <style scoped>
  #main {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  </style>
  