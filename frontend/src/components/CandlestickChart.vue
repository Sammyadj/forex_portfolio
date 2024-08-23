<template>
  <div ref="chartContainer" class="echart-container"></div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';
import { makeApiCall } from '@/stores/authHelpers';

export default {
  props: {
    instrument: {
      type: String,
      default: 'EUR/USD'
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
        // Call the token refresh logic and handle token expiration
        // await makeApiCall();

        // Now proceed with the actual API request using axios
        const response = await axios.get(`/api/trading/candles/${this.instrument.replace('/', '_')}/?count=100&granularity=${this.granularity}`);
        // console.log('Fetched data: ', response.data);
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
        series: [{
          name: this.instrument,
          type: 'candlestick',
          data: data.values,
          itemStyle: { color: '#00da3c', color0: '#ec0000', borderColor: '#008F28', borderColor0: '#8A0000' }
        }]
      };
    }
  },
  watch: {
    instrument(newVal, oldVal) {
      if (newVal !== oldVal) this.fetchChartData();
    },
    granularity(newVal, oldVal) {
      if (newVal !== oldVal) this.fetchChartData();
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

<style scoped>
.echart-container {
  width: 100%;
  height: 500px;
  border: 1px solid #dee2e6;
}
</style>






<!-- <template>
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
        console.log('Fetched data: ', response.data);
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
      if (!rawData) {
        console.error("No data available to process.");
        return { categoryData, values };
      }
      rawData.forEach(item => {
        if (!item.time || !item.open || !item.close || !item.low || !item.high) {
          console.error('Malformed data item:', item);
          return; // skip this iteration
        }
        categoryData.push(item.time.replace('T', ' ').replace('Z', ''));
        values.push([item.open, item.close, item.low, item.high]);
      });
      return { categoryData, values };
    },
    initChart(data) {
      console.log('Initializing chart with data:', data);
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
        title: { text: this.instrument, left: 0 },
        grid: {left: '10%', right: '5%', bottom: '15%'},
        tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
        xAxis: { type: 'category', data: data.categoryData, boundaryGap: false,
          axisLine: { onZero: false }, splitLine: { show: false }, min: 'dataMin', max: 'dataMax' },
        yAxis: { scale: true, splitArea: {show: true} },
        dataZoom: [
          {type: 'inside', start: 50, end: 100},
          {show: true, type: 'slider', top: '90%', start: 50, end: 100 }
        ],
        series: [{
          name: this.instrument,
          type: 'candlestick',
          data: data.values,
          itemStyle: { color: '#00da3c', color0: '#ec0000', borderColor: '#008F28', borderColor0: '#8A0000' }
        }]
      };
    },
    handleResize() {
      console.log('Handling resize');
      if (this.chart) {
        console.log('Resizing chart');
        this.chart.resize();
      }
    }
  },
  watch: {
    instrument(newVal, oldVal) {
      if (newVal !== oldVal) this.fetchChartData();
    },
    granularity(newVal, oldVal) {
      if (newVal !== oldVal) this.fetchChartData();
    }
  },
  mounted() {
    this.fetchChartData();
    // window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.dispose();
    }
    // window.removeEventListener('resize', this.handleResize);
  }
};
</script> -->



