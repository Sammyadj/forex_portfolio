<template>
  <div class="container mt-3">
    <div class="header text-center">
      <h1 class="mb-3">Real-Time Forex Prices</h1>
    </div>
    <div v-if="priceInfo" class="card-container d-flex flex-column align-items-start">
      <div v-for="(info, instrument) in priceInfo" :key="instrument" class="mb-3">
        <div class="card">
          <div class="card-header">
            {{ instrument }}
          </div>
          <div class="card-body">
            <p><strong>Bid:</strong> {{ info.bids[0].price }}</p>
            <p><strong>Ask:</strong> {{ info.asks[0].price }}</p>
          </div>
        </div>
      </div>
    </div>
    <p v-else class="text-muted">No price data available.</p>
  </div>
</template>


<script>
export default {
  data() {
    return {
      priceInfo: {},
      socket: null,
      instruments: ['EUR/USD', 'AUD/USD', 'GBP/USD', 'USD/JPY', 'GBP/JPY'],
    };
  },
  mounted() {
    this.connectWebSocket();
  },
  methods: {
    connectWebSocket() {
      this.socket = new WebSocket('ws://localhost:8000/ws/stream/pricing/');
      console.log('WebSocket created:');
      
      this.socket.onopen = () => {
        console.log('WebSocket is open now.');
        // Subscribe to multiple instruments
        this.socket.send(JSON.stringify({ action: 'subscribe', instruments: this.instruments }));
      };

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'PRICE') {
            // console.log('Received price data:', data);
            this.priceInfo[data.instrument] = data;
          }
        } catch (error) {
          console.error('Error parsing WebSocket data:', error);
        }
      };

      this.socket.onclose = function(event) {
        console.log("Socket is closed. Reconnect will be attempted in 1 second.", event.reason);
        setTimeout(function() {
          connectWebSocket();
        }, 1000);
      };

      this.socket.onerror = function(err) {
        console.error("Socket encountered error: ", err.message, "Closing socket");
        socket.close();
      };
    }
  },
  beforeDestroy() {
    if (this.socket) {
      this.socket.close();
    }
  }
};
</script>

<style scoped>
.card-header {
  background-color: #f7f7f7;
  color: #333;
  font-weight: bold;
}
.card {
  width: 200px; /* Adjust width as needed */
  border: 1px solid #dee2e6; /* Bootstrap's default border color */
}
.container {
  max-width: 100%; /* Use full width to allow centering */
}
.header {
  width: 100%; /* Full width to center the title */
}
.card-container {
  max-width: 250px; /* Adjust the container width to fit the cards */
}
.text-center {
  text-align: center; /* Center the text of the header */
}
</style>
