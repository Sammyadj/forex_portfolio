<template>
  <div class="trade-form">
    <button class="buy-button" @click="execute_trade('BUY', askPrice)">
      BUY <div class="buy-price">{{ askPrice }}</div>
    </button>
    <button class="sell-button" @click="execute_trade('SELL', bidPrice)">
      SELL <div class="sell-price">{{ bidPrice }}</div>
    </button>
  </div>
  <div>
    <p>Current Price: {{ currentPriceStream || 'loading...' }}</p>
  </div>
</template>

<script>
import { usePricingStore } from '@/stores/pricingStore';
import { useTradeStore } from '@/stores/tradeStore';
import { useProfileStore } from '@/stores/profile';
import { computed } from 'vue';

export default {
  props: {
    instrument: {
      type: String,
      default: 'EUR/USD'
    }
  },
  setup(props) {
    const pricingStore = usePricingStore();
    const tradeStore = useTradeStore();

    const profileStore = useProfileStore();
    const profileId = profileStore.profile?.id;

    // Computed properties to get the bid and ask price from the store
    const bidPrice = computed(() => pricingStore.prices[props.instrument]?.bid || 'Loading...');
    const askPrice = computed(() => pricingStore.prices[props.instrument]?.ask || 'Loading...');
    const currentPriceStream = computed(() => pricingStore.prices[props.instrument]?.currentPrice || 'Loading...');

    // Calculate the current price as the average of bid and ask prices
    const currentPrice = computed(() => {
      if (pricingStore.prices[props.instrument]) {
        return (pricingStore.prices[props.instrument].bid + pricingStore.prices[props.instrument].ask) / 2;
      }
      return 'Loading...';
    });

    function execute_trade(type, price) {
      console.log(`Attempting to ${type} ${props.instrument} at ${price}`);
      // trade submission logic here
      const data = {
        type,
        instrument: props.instrument,
        price,
        profile_id: profileId
      }
      tradeStore.openTradeCommand(data);
    }

    return {
      bidPrice,
      askPrice,
      // currentPrice,
      execute_trade,
      currentPriceStream
    };
  }
}
</script>

<style scoped>
.trade-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.buy-button, .sell-button {
  padding: 10px 20px;
  border: none;
  border-radius: 3px;  
  font-size: 16px;
  cursor: pointer;
  outline: none;
}

.buy-button {
  color: #1AC1FF;;
}
.sell-button {
  color: #FF1A1A;;
}

.buy-price, .sell-price {
  color: black;
}

.buy-button {
  background-color: #E4F7FE;
}

.sell-button {
  background-color: #FEE4E4;
}

/* .buy-button, .sell-button {
  width: 100%;
  padding: 10px 0;
} */

</style>
