<script setup lang="ts">
import { ref, onMounted } from 'vue';
import apiClient from '../service/config';
import { ElMessage, ElMessageBox } from 'element-plus';

interface Transaction {
  id: number;
  type: 'income' | 'expense';
  amount: number;
  description: string;
  date: string;
}

interface Stats {
  month: number;
  year: number;
  income: number;
  expense: number;
  balance: number;
}

const stats = ref<Stats>({ month: 0, year: 0, income: 0, expense: 0, balance: 0 });
const transactions = ref<Transaction[]>([]);
const newTransaction = ref<{
  type: 'income' | 'expense';
  amount: string | number;
  description: string;
  date: string;
}>({ 
  type: 'expense', 
  amount: '', 
  description: '',
  date: new Date().toISOString().split('T')[0] || ''
});
const loading = ref(false);

const fetchStats = async () => {
  try {
    const res = await apiClient.get('/stats/');
    stats.value = {
      month: res.data.month,
      year: res.data.year,
      income: parseFloat(res.data.income) || 0,
      expense: parseFloat(res.data.expense) || 0,
      balance: parseFloat(res.data.balance) || 0,
    };
  } catch (error) {
    console.error("Error fetching stats:", error);
  }
};

const fetchTransactions = async () => {
  try {
    const res = await apiClient.get('/list/');
    transactions.value = res.data.transactions.map((t: any) => ({
      ...t,
      amount: parseFloat(t.amount) || 0
    }));
  } catch (error) {
    console.error("Error fetching transactions:", error);
  }
};

const addTransaction = async () => {
  if (!newTransaction.value.amount) return;
  loading.value = true;
  try {
    await apiClient.post('/add/', {
      type: newTransaction.value.type,
      amount: parseFloat(newTransaction.value.amount.toString()),
      description: newTransaction.value.description,
      date: newTransaction.value.date
    });
    // Reset form but keep date
    newTransaction.value = { 
      type: 'expense', 
      amount: '', 
      description: '',
      date: newTransaction.value.date 
    };
    ElMessage.success('Transaction added successfully');
    await fetchStats();
    await fetchTransactions();
  } catch (error) {
    console.error("Error adding transaction:", error);
    ElMessage.error('Failed to add transaction');
  } finally {
    loading.value = false;
  }
};

const deleteTransaction = async (t: Transaction) => {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to delete this transaction?',
      'Warning',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning',
      }
    );
    
    await apiClient.post('/delete/', {
      id: t.id,
      type: t.type
    });
    
    ElMessage.success('Transaction deleted');
    await fetchStats();
    await fetchTransactions();
  } catch (error) {
    if (error !== 'cancel') {
      console.error("Error deleting transaction:", error);
      ElMessage.error('Failed to delete transaction');
    }
  }
};

const exportExcel = () => {
  window.location.href = `${apiClient.defaults.baseURL}/export/`;
};

onMounted(() => {
  fetchStats();
  fetchTransactions();
});
</script>

<template>
  <div class="dashboard">
    <header class="header">
      <h1>ClashFlow</h1>
      <button @click="exportExcel" class="btn btn-secondary">
        Export Excel
      </button>
    </header>

    <div class="stats-cards">
      <div class="card balance-card">
        <h3>Current Balance</h3>
        <div class="amount">{{ stats.balance.toFixed(2) }}</div>
        <div class="meta">{{ stats.month }}/{{ stats.year }}</div>
      </div>
      <div class="card income-card">
        <h3>Income</h3>
        <div class="amount">+{{ stats.income.toFixed(2) }}</div>
      </div>
      <div class="card expense-card">
        <h3>Expense</h3>
        <div class="amount">-{{ stats.expense.toFixed(2) }}</div>
      </div>
    </div>

    <div class="main-content">
      <div class="card form-card">
        <h2>New Transaction</h2>
        <form @submit.prevent="addTransaction" class="transaction-form">
          <div class="form-group">
            <label>Type</label>
            <div class="type-selector">
              <button 
                type="button" 
                :class="{ active: newTransaction.type === 'income' }"
                @click="newTransaction.type = 'income'"
              >Income</button>
              <button 
                type="button" 
                :class="{ active: newTransaction.type === 'expense' }"
                @click="newTransaction.type = 'expense'"
              >Expense</button>
            </div>
          </div>
          <div class="form-group">
            <label>Amount</label>
            <input v-model="newTransaction.amount" type="number" step="0.01" placeholder="0.00" required />
          </div>
          <div class="form-group">
            <label>Date</label>
            <input v-model="newTransaction.date" type="date" required />
          </div>
          <div class="form-group">
            <label>Description</label>
            <input v-model="newTransaction.description" type="text" placeholder="Note..." />
          </div>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Adding...' : 'Add Record' }}
          </button>
        </form>
      </div>

      <div class="card list-card">
        <h2>Recent Transactions</h2>
        <div class="transaction-list">
          <div v-for="t in transactions" :key="t.id" class="transaction-item">
            <div class="icon" :class="t.type">
              {{ t.type === 'income' ? '↓' : '↑' }}
            </div>
            <div class="details">
              <div class="desc">{{ t.description || 'No description' }}</div>
              <div class="date">{{ t.date }}</div>
            </div>
            <div class="amount" :class="t.type">
              {{ t.type === 'income' ? '+' : '-' }}{{ t.amount }}
            </div>
            <button class="delete-btn" @click="deleteTransaction(t)">×</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Apple Design System Inspired Styles */
:root {
  --bg-color: #f5f5f7;
  --card-bg: rgba(255, 255, 255, 0.8);
  --text-primary: #1d1d1f;
  --text-secondary: #86868b;
  --accent-blue: #0071e3;
  --accent-green: #34c759;
  --accent-red: #ff3b30;
  --radius: 18px;
  --shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
}

.dashboard {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif;
  color: #1d1d1f;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

h1 {
  font-size: 40px;
  font-weight: 700;
  letter-spacing: -0.5px;
  margin: 0;
}

h2 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
}

h3 {
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #86868b;
  margin-bottom: 8px;
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

.stats-cards {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 20px;
  margin-bottom: 40px;
}

.amount {
  font-size: 32px;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.balance-card .amount {
  font-size: 48px;
  background: linear-gradient(135deg, #1d1d1f 0%, #434344 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.income-card .amount { color: #34c759; }
.expense-card .amount { color: #ff3b30; }

.main-content {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 8px;
  color: #86868b;
}

input {
  width: 100%;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.5);
  font-size: 16px;
  transition: all 0.2s;
  box-sizing: border-box; /* Fix for width 100% padding issue */
}

input:focus {
  outline: none;
  border-color: #0071e3;
  background: #fff;
  box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1);
}

.type-selector {
  display: flex;
  background: rgba(118, 118, 128, 0.12);
  padding: 2px;
  border-radius: 10px;
}

.type-selector button {
  flex: 1;
  border: none;
  background: transparent;
  padding: 8px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s cubic-bezier(0.4, 0, 0.2, 1), transform 0.1s;
  outline: none; /* Remove default focus outline */
}

.type-selector button:focus {
  outline: none;
}

.type-selector button.active {
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}

.btn {
  border: none;
  padding: 12px 24px;
  border-radius: 99px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.1s;
}

.btn:active {
  transform: scale(0.98);
}

.btn-primary {
  background: #0071e3;
  color: #fff;
  width: 100%;
}

.btn-secondary {
  background: rgba(118, 118, 128, 0.12);
  color: #1d1d1f;
}

.transaction-list {
  max-height: 400px;
  overflow-y: auto;
}

.transaction-item {
  display: flex;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.transaction-item:last-child {
  border-bottom: none;
}

.icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  margin-right: 16px;
}

.icon.income { background: rgba(52, 199, 89, 0.1); color: #34c759; }
.icon.expense { background: rgba(255, 59, 48, 0.1); color: #ff3b30; }

.details {
  flex: 1;
}

.desc {
  font-weight: 500;
  font-size: 15px;
}

.date {
  font-size: 13px;
  color: #86868b;
  margin-top: 2px;
}

.transaction-item .amount {
  font-size: 16px;
}

.transaction-item .amount.income { color: #34c759; }
.transaction-item .amount.expense { color: #1d1d1f; } /* Apple style expenses usually neutral or black in lists */

.delete-btn {
  background: none;
  border: none;
  outline: none;
  color: #86868b;
  font-size: 24px;
  line-height: 1;
  padding: 0 0 0 16px;
  cursor: pointer;
  opacity: 0;
  transition: all 0.2s;
}

.delete-btn:focus {
  outline: none;
}

.transaction-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  color: #ff3b30;
}

/* Scrollbar styling */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}
</style>
