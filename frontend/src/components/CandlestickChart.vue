<template>
    <div ref="chartContainer" class="echart-container"></div>
</template>
  
<script>
import * as echarts from 'echarts';
import axios from 'axios';

export default {
  props: {
    instrument: {
      type: String,
      default: 'EUR_USD'
    },
    granularity: {
      type: String,
      default: 'H1'
    }
  },
  data() {
    return {
      chart: null,
    };
  },
  methods: {
    async fetchChartData() {
      try {
        const response = await axios.get(`/api/trading/candles/${this.instrument}/?count=100&granularity=${this.granularity}`);
        this.processAndRenderChart(response.data);
      } catch (error) {
        console.error('Error fetching candle data:', error);
      }
    },
    processAndRenderChart(rawData) {
      const processedData = this.processData(rawData);
      this.initChart(processedData);
    },
    processData(rawData) {
      const categoryData = [];
      const values = [];
      rawData.forEach(item => {
        categoryData.push(item.time.replace('T', ' ').replace('Z', ''));
        values.push([item.open, item.close, item.low, item.high]);
      });
      return { categoryData, values };
    },
    initChart(data) {
      if (!this.$refs.chartContainer) {
        console.error("Chart container ref is not available.");
        return;
      }
      if (this.chart) {
        this.chart.dispose();
      }
      this.chart = echarts.init(this.$refs.chartContainer);
      const option = this.getChartOption(data);
      this.chart.setOption(option, true);
    },
    getChartOption(data) {
      return {
        tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
        xAxis: { type: 'category', data: data.categoryData, scale: true },
        yAxis: { scale: true },
        dataZoom: [{ type: 'inside', start: 0, end: 100 }, { type: 'slider', start: 0, end: 100 }],
        series: [{
          name: this.instrument,
          type: 'candlestick',
          data: data.values,
          itemStyle: { color: '#00da3c', color0: '#ec0000', borderColor: '#008F28', borderColor0: '#8A0000' }
        }]
      };
    }
  },
  mounted() {
    this.fetchChartData();
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.dispose();
    }
  }
};
</script>

<style>
.echart-container {
  width: 1400px;
  height: 800px;
}
</style>


<!-- <script>
import * as echarts from 'echarts';
import axios from 'axios';

export default {
    props: {
        instrument: {
            type: String,
            default: 'EUR_USD'
        },
        granularity: {
            type: String,
            default: 'H1'
        }
    },
    name: 'CandlestickChart',
    data() {
        return {
            chart: null,
        };
    },
    methods: {
        async fetchChartData() {
            try {
                const response = await axios.get(`/api/trading/candles/${this.instrument}/?count=100&granularity=${this.granularity}`);
                console.log(`Fetching data from: /api/trading/candles/${this.instrument}/?count=100&granularity=${this.granularity}`);
                this.initChart(this.processData(response.data));
            } catch (error) {
                console.error('Error fetching candle data:', error);
            }
        },
        processData(rawData) {
            return rawData.map(item => {
                return [
                    item.time,
                    [item.open, item.close, item.low, item.high],
                ];
            });
        },
         processData(rawData) {
            const categoryData = [];
            const values = [];
            for (let item of rawData) {
                categoryData.push(item.time);
                values.push([item.open, item.close, item.low, item.high]);
            }
            return {
                categoryData,
                values,
                ma5: this.calculateMA(values, 5),
                ma10: this.calculateMA(values, 10),
            };
            },
        initChart(data) {
            const chartDom = this.$refs.chartContainer;
            if (this.chart) {
                this.chart.dispose();
            }
            this.chart = echarts.init(chartDom);
            const option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross'
                    }
                },
                xAxis: {
                    type: 'category',
                    data: data.map(item => item[0]),
                    scale: true,
                },
                yAxis: {
                    scale: true,
                },
                series: [
                    {
                        name: this.instrument,
                        type: 'candlestick',
                        data: data.map(item => item[1]),
                        itemStyle: {
                            color: '#00da3c',
                            color0: '#ec0000',
                            borderColor: '#008F28',
                            borderColor0: '#8A0000'
                        }
                    }
                ]
            };
            this.chart.setOption(option);
        },
    },
    watch: {
        granularity(newVal) {
            this.fetchChartData();
        },
        instrument(newVal) {
            this.fetchChartData();
        }
    },
    mounted() {
        this.fetchChartData();
    },
    beforeUnmount() {
        if (this.chart) {
            this.chart.dispose();
        }
    },
};
</script> -->




