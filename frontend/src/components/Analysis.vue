<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement
} from 'chart.js';
import { Line, Doughnut } from 'vue-chartjs';
import apiClient from '../service/config';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

interface Transaction {
  id: number;
  type: 'income' | 'expense';
  amount: number;
  description: string;
  date: string;
}

const transactions = ref<Transaction[]>([]);
const loading = ref(true);

const fetchTransactions = async () => {
  try {
    loading.value = true;
    const res = await apiClient.get('/list/');
    transactions.value = res.data.transactions.map((t: any) => ({
      ...t,
      amount: parseFloat(t.amount) || 0
    }));
  } catch (error) {
    console.error("Error fetching transactions:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchTransactions();
});

// Chart Data Processors

// 1. Line Chart: Daily Income vs Expense
const dailyChartData = computed(() => {
  const dates = [...new Set(transactions.value.map(t => t.date))].sort();
  // Limit to last 30 days for better visibility
  const last30Days = dates.slice(-30);

  const incomeData = last30Days.map(date => {
    return transactions.value
      .filter(t => t.date === date && t.type === 'income')
      .reduce((sum, t) => sum + t.amount, 0);
  });

  const expenseData = last30Days.map(date => {
    return transactions.value
      .filter(t => t.date === date && t.type === 'expense')
      .reduce((sum, t) => sum + t.amount, 0);
  });

  return {
    labels: last30Days,
    datasets: [
      {
        label: 'Income',
        backgroundColor: '#34c759',
        borderColor: '#34c759',
        data: incomeData,
        tension: 0.4
      },
      {
        label: 'Expense',
        backgroundColor: '#ff3b30',
        borderColor: '#ff3b30',
        data: expenseData,
        tension: 0.4
      }
    ]
  };
});

// 2. Doughnut Chart: Expense vs Income Total
const totalDistributionData = computed(() => {
  const totalIncome = transactions.value
    .filter(t => t.type === 'income')
    .reduce((sum, t) => sum + t.amount, 0);
    
  const totalExpense = transactions.value
    .filter(t => t.type === 'expense')
    .reduce((sum, t) => sum + t.amount, 0);

  return {
    labels: ['Income', 'Expense'],
    datasets: [
      {
        backgroundColor: ['#34c759', '#ff3b30'],
        data: [totalIncome, totalExpense]
      }
    ]
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
};
</script>

<template>
  <div class="analysis-page">
    <header class="header">
      <h1>Data Analysis</h1>
    </header>

    <div v-if="loading" class="loading">Loading data...</div>
    
    <div v-else class="charts-container">
      <div class="card chart-card wide">
        <h3>Income vs Expense (Last 30 Days)</h3>
        <div class="chart-wrapper">
          <Line :data="dailyChartData" :options="chartOptions" />
        </div>
      </div>

      <div class="card chart-card">
        <h3>Total Distribution</h3>
        <div class="chart-wrapper">
          <Doughnut :data="totalDistributionData" :options="chartOptions" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.analysis-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif;
  color: #1d1d1f;
}

.header {
  margin-bottom: 40px;
}

h1 {
  font-size: 40px;
  font-weight: 700;
  letter-spacing: -0.5px;
  margin: 0;
}

h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #86868b;
}

.card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.4);
}

.charts-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.chart-card {
  height: 400px;
  display: flex;
  flex-direction: column;
}

.chart-wrapper {
  flex: 1;
  position: relative;
  min-height: 0; /* Important for Chart.js in Flex/Grid */
}

.wide {
  grid-column: span 1;
}

@media (max-width: 768px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
}
</style>
