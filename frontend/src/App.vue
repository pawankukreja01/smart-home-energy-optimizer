<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue"
import axios from "axios"
import EnergyChart from "./EnergyChart.vue"

const API_BASE = "http://127.0.0.1:8000/api"

const devices = ref([])
const analytics = ref({})
const automationHistory = ref([])
const energySavings = ref([])
const savingsAnalytics = ref({
  total_energy_saved_kwh: 0,
  total_cost_saved: 0,
  total_power_avoided_watts: 0,
  automation_actions: 0,
  completed_savings: 0,
  active_savings: 0,
})

const loading = ref(true)
const error = ref("")
let refreshInterval = null


// ========================================
// API FUNCTIONS
// ========================================

const fetchDevices = async () => {
  try {
    const response = await axios.get(
      `${API_BASE}/devices/`
    )

    devices.value = response.data
    error.value = ""
  } catch (err) {
    console.error("Failed to fetch devices:", err)
    error.value =
      "Unable to connect to the smart home system."
  }
}


const fetchAnalytics = async () => {
  try {
    const response = await axios.get(
      `${API_BASE}/analytics/`
    )

    analytics.value = response.data
  } catch (err) {
    console.error(
      "Failed to fetch analytics:",
      err
    )
  }
}


const fetchAutomationHistory = async () => {
  try {
    const response = await axios.get(
      `${API_BASE}/automation-history/`
    )

    automationHistory.value = response.data
  } catch (err) {
    console.error(
      "Failed to fetch automation history:",
      err
    )
  }
}


const fetchEnergySavings = async () => {
  try {
    const response = await axios.get(
      `${API_BASE}/energy-savings/`
    )

    energySavings.value = response.data
  } catch (err) {
    console.error(
      "Failed to fetch energy savings:",
      err
    )
  }
}


const fetchSavingsAnalytics = async () => {
  try {
    const response = await axios.get(
      `${API_BASE}/energy-savings-analytics/`
    )

    savingsAnalytics.value = response.data
  } catch (err) {
    console.error(
      "Failed to fetch savings analytics:",
      err
    )
  }
}


// ========================================
// DEVICE CONTROL
// ========================================

const getDefaultPower = (device) => {
  const defaults = {
    light: 40,
    ac: 850,
    tv: 100,
    thermostat: 3,
    appliance: 500,
  }

  return defaults[device.device_type] || 0
}


const toggleDevice = async (device) => {
  try {
    const turningOn = !device.is_on

    await axios.patch(
      `${API_BASE}/devices/${device.id}/`,
      {
        is_on: turningOn,
        power_watts: turningOn
          ? getDefaultPower(device)
          : 0,
      }
    )

    await Promise.all([
      fetchDevices(),
      fetchEnergySavings(),
      fetchSavingsAnalytics(),
    ])

  } catch (err) {
    console.error(
      "Failed to toggle device:",
      err
    )

    error.value =
      "Unable to control device."
  }
}


// ========================================
// COMPUTED VALUES
// ========================================

const totalPower = computed(() => {
  return devices.value.reduce(
    (total, device) =>
      total + Number(device.power_watts || 0),
    0
  )
})


const activeDevices = computed(() => {
  return devices.value.filter(
    device => device.is_on
  ).length
})


const totalDevices = computed(() => {
  return devices.value.length
})


const hasAnomaly = computed(() => {
  return (
    analytics.value &&
    analytics.value.latest_anomaly
  )
})


// ========================================
// HELPERS
// ========================================

const formatTime = (timestamp) => {
  if (!timestamp) {
    return "—"
  }

  return new Date(
    timestamp
  ).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  })
}


const formatDuration = (hours) => {
  const value = Number(hours || 0)

  if (value <= 0) {
    return "—"
  }

  if (value < 1) {
    const minutes = Math.round(
      value * 60
    )

    return `${minutes} min`
  }

  return `${value.toFixed(2)} hrs`
}


// ========================================
// LIFECYCLE
// ========================================

onMounted(async () => {
  loading.value = true

  await Promise.all([
    fetchDevices(),
    fetchAnalytics(),
    fetchAutomationHistory(),
    fetchEnergySavings(),
    fetchSavingsAnalytics(),
  ])

  loading.value = false

  refreshInterval = setInterval(() => {
    fetchDevices()
    fetchAnalytics()
    fetchAutomationHistory()
    fetchEnergySavings()
    fetchSavingsAnalytics()
  }, 5000)
})


onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>


<template>
  <div class="dashboard">

    <!-- ================================= -->
    <!-- HEADER -->
    <!-- ================================= -->

    <header class="header">

      <div class="title-row">

        <div class="home-icon">
          🏠
        </div>

        <div>
          <h1>
            AI Smart Home
            <span>Energy Optimizer</span>
          </h1>

          <p class="subtitle">
            Intelligent energy monitoring,
            anomaly detection & automation
          </p>
        </div>

      </div>


      <div class="system-status">
        <span class="status-dot"></span>
        System Online
      </div>

    </header>


    <!-- ================================= -->
    <!-- ERROR -->
    <!-- ================================= -->

    <div
      v-if="error"
      class="error-message"
    >
      ⚠️ {{ error }}
    </div>


    <!-- ================================= -->
    <!-- TOP SUMMARY -->
    <!-- ================================= -->

    <section class="summary-grid">

      <div class="summary-card">

        <div class="summary-icon">
          ⚡
        </div>

        <div>

          <p class="summary-label">
            Current Power
          </p>

          <h2>
            {{ totalPower.toFixed(1) }}
            <span>W</span>
          </h2>

        </div>

      </div>


      <div class="summary-card">

        <div class="summary-icon">
          💡
        </div>

        <div>

          <p class="summary-label">
            Active Devices
          </p>

          <h2>
            {{ activeDevices }}
            <span>/ {{ totalDevices }}</span>
          </h2>

        </div>

      </div>


      <div class="summary-card">

        <div class="summary-icon">
          🤖
        </div>

        <div>

          <p class="summary-label">
            AI Alerts
          </p>

          <h2>
            {{ analytics.alert_count || 0 }}
          </h2>

        </div>

      </div>


      <div class="summary-card">

        <div class="summary-icon">
          📉
        </div>

        <div>

          <p class="summary-label">
            Power Avoided
          </p>

          <h2>
            {{
              Number(
                savingsAnalytics
                  .total_power_avoided_watts || 0
              ).toFixed(1)
            }}
            <span>W</span>
          </h2>

        </div>

      </div>

    </section>


    <!-- ================================= -->
    <!-- ENERGY CHART -->
    <!-- ================================= -->

    <section class="panel">

      <div class="panel-header">

        <div>
          <h2>
            ⚡ Energy Consumption
          </h2>

          <p>
            Real-time energy usage from simulated
            smart home devices
          </p>
        </div>

        <div class="live-badge">
          LIVE
        </div>

      </div>

      <div class="chart-container">
        <EnergyChart />
      </div>

    </section>


    <!-- ================================= -->
    <!-- ENERGY INSIGHTS -->
    <!-- ================================= -->

    <section class="panel insights-panel">

      <div class="panel-header">

        <div>
          <h2>
            💰 Energy Insights
          </h2>

          <p>
            Cumulative impact of automated
            energy-saving actions
          </p>
        </div>

        <div class="saving-rate">
          £0.30 / kWh
        </div>

      </div>


      <div class="insights-grid">

        <!-- ENERGY SAVED -->

        <div class="insight-card">

          <div class="insight-icon">
            ⚡
          </div>

          <div>

            <span>
              Energy Saved
            </span>

            <strong>
              {{
                Number(
                  savingsAnalytics
                    .total_energy_saved_kwh || 0
                ).toFixed(4)
              }}
              <small>kWh</small>
            </strong>

          </div>

        </div>


        <!-- COST SAVED -->

        <div class="insight-card">

          <div class="insight-icon">
            💷
          </div>

          <div>

            <span>
              Estimated Cost Saved
            </span>

            <strong class="money">
              £{{
                Number(
                  savingsAnalytics
                    .total_cost_saved || 0
                ).toFixed(4)
              }}
            </strong>

          </div>

        </div>


        <!-- POWER AVOIDED -->

        <div class="insight-card">

          <div class="insight-icon">
            📉
          </div>

          <div>

            <span>
              Power Avoided
            </span>

            <strong>
              {{
                Number(
                  savingsAnalytics
                    .total_power_avoided_watts || 0
                ).toFixed(1)
              }}
              <small>W</small>
            </strong>

          </div>

        </div>


        <!-- AUTOMATIONS -->

        <div class="insight-card">

          <div class="insight-icon">
            🤖
          </div>

          <div>

            <span>
              Automation Actions
            </span>

            <strong>
              {{
                savingsAnalytics
                  .automation_actions || 0
              }}
            </strong>

          </div>

        </div>

      </div>


      <!-- STATUS -->

      <div class="savings-status">

        <div>
          <span class="status-indicator completed"></span>

          <strong>
            {{
              savingsAnalytics
                .completed_savings || 0
            }}
          </strong>

          completed savings periods
        </div>


        <div>
          <span class="status-indicator active"></span>

          <strong>
            {{
              savingsAnalytics
                .active_savings || 0
            }}
          </strong>

          active savings periods
        </div>

      </div>


      <div class="estimate-note">
        * Cost savings are estimates based on
        an electricity rate of £0.30 per kWh.
      </div>

    </section>


    <!-- ================================= -->
    <!-- SAVINGS HISTORY -->
    <!-- ================================= -->

    <section class="panel">

      <div class="panel-header">

        <div>
          <h2>
            📊 Savings History
          </h2>

          <p>
            Energy savings generated by the
            automation engine
          </p>
        </div>

        <div class="action-count">
          {{ energySavings.length }}
          records
        </div>

      </div>


      <div
        v-if="energySavings.length > 0"
        class="savings-list"
      >

        <div
          v-for="saving in energySavings"
          :key="saving.id"
          class="saving-row"
        >

          <div class="saving-device">

            <div class="device-small-icon">
              ⚡
            </div>

            <div>

              <strong>
                {{ saving.device_name }}
              </strong>

              <span>
                Automated energy saving
              </span>

            </div>

          </div>


          <div class="saving-stat">

            <span>
              Power
            </span>

            <strong>
              {{
                Number(
                  saving.power_saved_watts || 0
                ).toFixed(1)
              }}
              W
            </strong>

          </div>


          <div class="saving-stat">

            <span>
              Duration
            </span>

            <strong>
              {{
                formatDuration(
                  saving.duration_hours
                )
              }}
            </strong>

          </div>


          <div class="saving-stat">

            <span>
              Energy
            </span>

            <strong>
              {{
                Number(
                  saving.energy_saved_kwh || 0
                ).toFixed(4)
              }}
              kWh
            </strong>

          </div>


          <div class="saving-stat">

            <span>
              Cost
            </span>

            <strong class="money">
              £{{
                Number(
                  saving.estimated_cost_saved || 0
                ).toFixed(4)
              }}
            </strong>

          </div>


          <div class="saving-time">
            {{ formatTime(saving.timestamp) }}
          </div>

        </div>

      </div>


      <div
        v-else
        class="empty-state"
      >

        <div>
          💡
        </div>

        <p>
          No energy savings recorded yet.
        </p>

        <span>
          Automated energy-saving actions
          will appear here.
        </span>

      </div>

    </section>


    <!-- ================================= -->
    <!-- AI ENERGY MONITOR -->
    <!-- ================================= -->

    <section class="panel">

      <div class="panel-header">

        <div>
          <h2>
            🤖 AI Energy Monitor
          </h2>

          <p>
            Machine learning powered
            anomaly detection
          </p>
        </div>


        <div
          class="ai-status"
          :class="{
            alert: hasAnomaly,
            normal: !hasAnomaly
          }"
        >

          <span></span>

          {{
            hasAnomaly
              ? "Anomaly Detected"
              : "All Systems Normal"
          }}

        </div>

      </div>


      <!-- ANOMALY -->

      <div
        v-if="hasAnomaly"
        class="anomaly-card"
      >

        <div class="anomaly-header">

          <div class="warning-icon">
            🚨
          </div>

          <div>

            <h3>
              {{
                analytics
                  .latest_anomaly
                  .device
              }}
            </h3>

            <p>
              Unusual energy consumption detected
            </p>

          </div>

        </div>


        <div class="anomaly-stats">

          <div>

            <span>
              Current Consumption
            </span>

            <strong>
              {{
                Number(
                  analytics
                    .latest_anomaly
                    .power_watts
                ).toFixed(1)
              }}
              W
            </strong>

          </div>


          <div>

            <span>
              Normal Range
            </span>

            <strong>
              {{
                analytics
                  .latest_anomaly
                  .normal_min_watts
              }}
              –
              {{
                analytics
                  .latest_anomaly
                  .normal_max_watts
              }}
              W
            </strong>

          </div>


          <div>

            <span>
              Potential Saving
            </span>

            <strong>
              {{
                Number(
                  analytics
                    .latest_anomaly
                    .potential_saving_watts
                ).toFixed(1)
              }}
              W
            </strong>

          </div>

        </div>


        <div class="recommendation">

          <span>
            💡 AI Recommendation
          </span>

          <p>
            {{ analytics.recommendation }}
          </p>

        </div>


        <div class="automation-message">
          🤖 Automation engine can respond
          automatically to this anomaly.
        </div>

      </div>


      <!-- NORMAL -->

      <div
        v-else
        class="normal-card"
      >

        <div class="normal-icon">
          ✓
        </div>

        <div>

          <h3>
            Energy consumption looks normal
          </h3>

          <p>
            The AI monitoring system has not
            detected unusual consumption patterns.
          </p>

        </div>

      </div>

    </section>


    <!-- ================================= -->
    <!-- AUTOMATION HISTORY -->
    <!-- ================================= -->

    <section class="panel">

      <div class="panel-header">

        <div>
          <h2>
            ⚙️ Automation History
          </h2>

          <p>
            Actions performed by the
            automation engine
          </p>
        </div>

        <div class="action-count">
          {{ automationHistory.length }}
          actions
        </div>

      </div>


      <div
        v-if="automationHistory.length > 0"
        class="automation-list"
      >

        <div
          v-for="action in automationHistory"
          :key="action.id"
          class="automation-row"
        >

          <div class="automation-icon">
            🤖
          </div>


          <div class="automation-main">

            <strong>
              {{ action.device_name }}
            </strong>

            <span>
              {{ action.action_type }}
            </span>

            <p>
              {{ action.reason }}
            </p>

          </div>


          <div class="automation-power">

            <div>

              <span>
                Before
              </span>

              <strong>
                {{
                  Number(
                    action.power_before || 0
                  ).toFixed(1)
                }}
                W
              </strong>

            </div>


            <div>

              <span>
                After
              </span>

              <strong>
                {{
                  Number(
                    action.power_after || 0
                  ).toFixed(1)
                }}
                W
              </strong>

            </div>


            <div class="saved-power">

              <span>
                Saved
              </span>

              <strong>
                {{
                  Number(
                    action.potential_saving_watts || 0
                  ).toFixed(1)
                }}
                W
              </strong>

            </div>

          </div>


          <div class="automation-time">
            {{ formatTime(action.timestamp) }}
          </div>

        </div>

      </div>


      <div
        v-else
        class="empty-state"
      >

        <div>
          ⚙️
        </div>

        <p>
          No automation actions yet.
        </p>

        <span>
          AI-triggered device actions will
          appear here.
        </span>

      </div>

    </section>


    <!-- ================================= -->
    <!-- DEVICES -->
    <!-- ================================= -->

    <section class="panel">

      <div class="panel-header">

        <div>
          <h2>
            🏠 Smart Devices
          </h2>

          <p>
            Monitor and control connected devices
          </p>
        </div>

        <div class="device-count">
          {{ activeDevices }} active
        </div>

      </div>


      <div class="devices-grid">

        <div
          v-for="device in devices"
          :key="device.id"
          class="device-card"
          :class="{
            active: device.is_on
          }"
        >

          <div class="device-top">

            <div
              class="device-icon"
              :class="{
                on: device.is_on
              }"
            >

              <span
                v-if="device.device_type === 'light'"
              >
                💡
              </span>

              <span
                v-else-if="device.device_type === 'ac'"
              >
                ❄️
              </span>

              <span
                v-else-if="device.device_type === 'tv'"
              >
                📺
              </span>

              <span
                v-else-if="
                  device.device_type === 'thermostat'
                "
              >
                🌡️
              </span>

              <span v-else>
                🔌
              </span>

            </div>


            <div
              class="device-state"
              :class="{
                on: device.is_on
              }"
            >
              {{ device.is_on ? "ON" : "OFF" }}
            </div>

          </div>


          <div class="device-info">

            <h3>
              {{ device.name }}
            </h3>

            <p>
              {{ device.room }}
            </p>

          </div>


          <div class="device-power">

            <strong>
              {{
                Number(
                  device.power_watts || 0
                ).toFixed(1)
              }}
              W
            </strong>

            <span>
              Current consumption
            </span>

          </div>


          <button
            class="toggle-button"
            :class="{
              on: device.is_on
            }"
            @click="toggleDevice(device)"
          >
            {{
              device.is_on
                ? "Turn Off"
                : "Turn On"
            }}
          </button>

        </div>

      </div>

    </section>


    <!-- ================================= -->
    <!-- FOOTER -->
    <!-- ================================= -->

    <footer class="footer">

      <span>
        AI Smart Home Energy Optimizer
      </span>

      <span>
        Django • Vue.js • Scikit-learn
      </span>

    </footer>

  </div>
</template>


<style>
/* =========================================
   GLOBAL
========================================= */

* {
  box-sizing: border-box;
}

body {
  margin: 0;

  font-family:
    Inter,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;

  background: #07111f;
  color: #e5e7eb;
}

button {
  font-family: inherit;
}

.dashboard {
  min-height: 100vh;

  padding: 32px;

  max-width: 1500px;
  margin: 0 auto;
}


/* =========================================
   HEADER
========================================= */

.header {
  display: flex;

  justify-content: space-between;
  align-items: center;

  margin-bottom: 32px;
}

.title-row {
  display: flex;

  align-items: center;

  gap: 16px;
}

.home-icon {
  width: 56px;
  height: 56px;

  display: flex;

  align-items: center;
  justify-content: center;

  background: #0f2438;

  border: 1px solid #1d3a52;

  border-radius: 16px;

  font-size: 27px;
}

.header h1 {
  margin: 0;

  font-size: 28px;
  font-weight: 700;

  letter-spacing: -0.5px;
}

.header h1 span {
  color: #38bdf8;
}

.subtitle {
  margin: 6px 0 0;

  color: #8fa3b8;

  font-size: 14px;
}

.system-status {
  display: flex;

  align-items: center;

  gap: 8px;

  padding: 10px 15px;

  border: 1px solid #174c3b;

  border-radius: 999px;

  background: #09231c;

  color: #67e8a5;

  font-size: 13px;
}

.status-dot {
  width: 8px;
  height: 8px;

  border-radius: 50%;

  background: #34d399;

  box-shadow: 0 0 10px #34d399;
}


/* =========================================
   ERROR
========================================= */

.error-message {
  margin-bottom: 20px;

  padding: 14px 18px;

  background: #32151a;

  border: 1px solid #6b252d;

  border-radius: 12px;

  color: #fca5a5;
}


/* =========================================
   SUMMARY
========================================= */

.summary-grid {
  display: grid;

  grid-template-columns:
    repeat(4, minmax(0, 1fr));

  gap: 18px;

  margin-bottom: 22px;
}

.summary-card {
  display: flex;

  align-items: center;

  gap: 16px;

  padding: 22px;

  background: #0b1929;

  border: 1px solid #173047;

  border-radius: 16px;

  transition:
    transform 0.2s,
    border-color 0.2s;
}

.summary-card:hover {
  transform: translateY(-2px);

  border-color: #27506e;
}

.summary-icon {
  width: 48px;
  height: 48px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 13px;

  background: #10283c;

  font-size: 22px;
}

.summary-label {
  margin: 0 0 5px;

  color: #8298ad;

  font-size: 13px;
}

.summary-card h2 {
  margin: 0;

  font-size: 25px;
  font-weight: 700;
}

.summary-card h2 span {
  color: #7890a4;

  font-size: 13px;

  font-weight: 500;
}


/* =========================================
   PANELS
========================================= */

.panel {
  margin-bottom: 22px;

  padding: 24px;

  background: #0b1929;

  border: 1px solid #173047;

  border-radius: 18px;
}

.panel-header {
  display: flex;

  align-items: flex-start;

  justify-content: space-between;

  margin-bottom: 22px;
}

.panel-header h2 {
  margin: 0;

  font-size: 19px;
}

.panel-header p {
  margin: 6px 0 0;

  color: #8196aa;

  font-size: 13px;
}

.live-badge,
.action-count,
.device-count,
.saving-rate {
  padding: 7px 11px;

  border-radius: 8px;

  background: #10283b;

  color: #71c9f4;

  font-size: 11px;

  font-weight: 700;
}

.live-badge {
  color: #67e8a5;

  background: #09271f;
}

.chart-container {
  min-height: 300px;
}


/* =========================================
   ENERGY INSIGHTS
========================================= */

.insights-panel {
  border-color: #193b4d;
}

.insights-grid {
  display: grid;

  grid-template-columns:
    repeat(4, minmax(0, 1fr));

  gap: 14px;
}

.insight-card {
  display: flex;

  align-items: center;

  gap: 14px;

  padding: 19px;

  background: #091725;

  border: 1px solid #173447;

  border-radius: 14px;
}

.insight-icon {
  width: 43px;
  height: 43px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 11px;

  background: #102b3d;

  font-size: 19px;
}

.insight-card span {
  display: block;

  margin-bottom: 5px;

  color: #8298ad;

  font-size: 11px;
}

.insight-card strong {
  display: block;

  font-size: 19px;
}

.insight-card strong small {
  color: #7c91a4;

  font-size: 11px;

  font-weight: 500;
}

.money {
  color: #67e8a5;
}

.savings-status {
  display: flex;

  gap: 25px;

  margin-top: 18px;

  padding: 14px 16px;

  background: #091725;

  border: 1px solid #173447;

  border-radius: 10px;

  color: #71879b;

  font-size: 11px;
}

.savings-status > div {
  display: flex;

  align-items: center;

  gap: 7px;
}

.savings-status strong {
  color: #dce7ef;
}

.status-indicator {
  width: 7px;
  height: 7px;

  border-radius: 50%;
}

.status-indicator.completed {
  background: #34d399;
}

.status-indicator.active {
  background: #38bdf8;
}

.estimate-note {
  margin-top: 13px;

  color: #62788d;

  font-size: 10px;
}


/* =========================================
   SAVINGS HISTORY
========================================= */

.savings-list {
  display: flex;

  flex-direction: column;

  gap: 1px;

  overflow: hidden;

  border: 1px solid #173047;

  border-radius: 13px;
}

.saving-row {
  display: grid;

  grid-template-columns:
    2fr
    1fr
    1fr
    1fr
    1fr
    auto;

  align-items: center;

  gap: 18px;

  padding: 17px;

  background: #091725;

  border-bottom: 1px solid #142a3d;
}

.saving-row:last-child {
  border-bottom: none;
}

.saving-device {
  display: flex;

  align-items: center;

  gap: 12px;
}

.device-small-icon {
  width: 38px;
  height: 38px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 10px;

  background: #10283a;
}

.saving-device strong {
  display: block;

  font-size: 14px;
}

.saving-device span {
  display: block;

  margin-top: 4px;

  color: #71879b;

  font-size: 11px;
}

.saving-stat span {
  display: block;

  margin-bottom: 4px;

  color: #71879b;

  font-size: 10px;

  text-transform: uppercase;

  letter-spacing: 0.4px;
}

.saving-stat strong {
  font-size: 13px;
}

.saving-time {
  color: #71879b;

  font-size: 11px;

  white-space: nowrap;
}

.empty-state {
  padding: 35px 20px;

  text-align: center;

  border: 1px dashed #244057;

  border-radius: 13px;

  background: #091725;
}

.empty-state div {
  margin-bottom: 10px;

  font-size: 25px;
}

.empty-state p {
  margin: 0 0 5px;

  font-weight: 600;
}

.empty-state span {
  color: #71879b;

  font-size: 12px;
}


/* =========================================
   AI MONITOR
========================================= */

.ai-status {
  display: flex;

  align-items: center;

  gap: 7px;

  padding: 7px 11px;

  border-radius: 8px;

  font-size: 11px;

  font-weight: 600;
}

.ai-status span {
  width: 7px;
  height: 7px;

  border-radius: 50%;
}

.ai-status.normal {
  background: #09271f;

  color: #67e8a5;
}

.ai-status.normal span {
  background: #34d399;
}

.ai-status.alert {
  background: #321d10;

  color: #fdba74;
}

.ai-status.alert span {
  background: #fb923c;
}

.anomaly-card {
  padding: 20px;

  background: #1c1510;

  border: 1px solid #62401d;

  border-radius: 14px;
}

.anomaly-header {
  display: flex;

  align-items: center;

  gap: 14px;

  margin-bottom: 20px;
}

.warning-icon {
  width: 44px;
  height: 44px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 11px;

  background: #34200f;

  font-size: 21px;
}

.anomaly-header h3 {
  margin: 0;

  font-size: 16px;
}

.anomaly-header p {
  margin: 4px 0 0;

  color: #9e876d;

  font-size: 12px;
}

.anomaly-stats {
  display: grid;

  grid-template-columns:
    repeat(3, 1fr);

  gap: 12px;

  margin-bottom: 18px;
}

.anomaly-stats > div {
  padding: 14px;

  background: #17120e;

  border: 1px solid #3c2a19;

  border-radius: 10px;
}

.anomaly-stats span {
  display: block;

  margin-bottom: 6px;

  color: #9e876d;

  font-size: 11px;
}

.anomaly-stats strong {
  font-size: 16px;
}

.recommendation {
  padding: 15px;

  background: #10202c;

  border-radius: 10px;
}

.recommendation > span {
  color: #7dd3fc;

  font-size: 12px;

  font-weight: 600;
}

.recommendation p {
  margin: 8px 0 0;

  color: #c6d2dd;

  font-size: 13px;

  line-height: 1.5;
}

.automation-message {
  margin-top: 14px;

  color: #fdba74;

  font-size: 12px;
}

.normal-card {
  display: flex;

  align-items: center;

  gap: 16px;

  padding: 20px;

  background: #09231c;

  border: 1px solid #174c3b;

  border-radius: 14px;
}

.normal-icon {
  width: 44px;
  height: 44px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background: #0d392c;

  color: #67e8a5;

  font-size: 21px;
}

.normal-card h3 {
  margin: 0 0 5px;

  font-size: 15px;
}

.normal-card p {
  margin: 0;

  color: #78998c;

  font-size: 12px;
}


/* =========================================
   AUTOMATION HISTORY
========================================= */

.automation-list {
  display: flex;

  flex-direction: column;

  gap: 1px;

  overflow: hidden;

  border: 1px solid #173047;

  border-radius: 13px;
}

.automation-row {
  display: grid;

  grid-template-columns:
    auto
    1fr
    auto
    auto;

  align-items: center;

  gap: 18px;

  padding: 17px;

  background: #091725;

  border-bottom: 1px solid #142a3d;
}

.automation-row:last-child {
  border-bottom: none;
}

.automation-icon {
  width: 40px;
  height: 40px;

  display: flex;

  align-items: center;
  justify-content: center;

  background: #10283b;

  border-radius: 10px;
}

.automation-main strong {
  display: block;

  font-size: 14px;
}

.automation-main > span {
  display: inline-block;

  margin-top: 4px;

  color: #67e8a5;

  font-size: 10px;
}

.automation-main p {
  margin: 6px 0 0;

  color: #75899b;

  font-size: 11px;
}

.automation-power {
  display: flex;

  gap: 20px;
}

.automation-power div {
  text-align: right;
}

.automation-power span {
  display: block;

  margin-bottom: 4px;

  color: #687d90;

  font-size: 10px;
}

.automation-power strong {
  font-size: 12px;
}

.saved-power strong {
  color: #67e8a5;
}

.automation-time {
  color: #687d90;

  font-size: 11px;

  white-space: nowrap;
}


/* =========================================
   DEVICES
========================================= */

.devices-grid {
  display: grid;

  grid-template-columns:
    repeat(4, minmax(0, 1fr));

  gap: 16px;
}

.device-card {
  padding: 18px;

  background: #091725;

  border: 1px solid #173047;

  border-radius: 14px;

  transition:
    transform 0.2s,
    border-color 0.2s;
}

.device-card:hover {
  transform: translateY(-2px);
}

.device-card.active {
  border-color: #24536d;
}

.device-top {
  display: flex;

  justify-content: space-between;

  align-items: center;
}

.device-icon {
  width: 45px;
  height: 45px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 12px;

  background: #102334;

  font-size: 21px;
}

.device-icon.on {
  background: #123347;
}

.device-state {
  padding: 5px 8px;

  border-radius: 6px;

  background: #1a2028;

  color: #788797;

  font-size: 10px;

  font-weight: 700;
}

.device-state.on {
  background: #092a21;

  color: #67e8a5;
}

.device-info {
  margin-top: 17px;
}

.device-info h3 {
  margin: 0;

  font-size: 14px;
}

.device-info p {
  margin: 4px 0 0;

  color: #71869a;

  font-size: 11px;
}

.device-power {
  display: flex;

  justify-content: space-between;

  align-items: flex-end;

  margin-top: 18px;
}

.device-power strong {
  font-size: 18px;
}

.device-power span {
  color: #607588;

  font-size: 9px;

  text-align: right;
}

.toggle-button {
  width: 100%;

  margin-top: 17px;

  padding: 9px;

  border: 1px solid #284258;

  border-radius: 8px;

  background: #102131;

  color: #b5c4d1;

  cursor: pointer;

  font-size: 11px;

  font-weight: 600;

  transition: 0.2s;
}

.toggle-button:hover {
  background: #163047;
}

.toggle-button.on {
  background: #102d29;

  border-color: #21604e;

  color: #67e8a5;
}


/* =========================================
   FOOTER
========================================= */

.footer {
  display: flex;

  justify-content: space-between;

  padding: 10px 4px 25px;

  color: #536a7e;

  font-size: 11px;
}


/* =========================================
   RESPONSIVE
========================================= */

@media (max-width: 1100px) {

  .summary-grid {
    grid-template-columns:
      repeat(2, 1fr);
  }

  .insights-grid {
    grid-template-columns:
      repeat(2, 1fr);
  }

  .devices-grid {
    grid-template-columns:
      repeat(2, 1fr);
  }

  .saving-row {
    grid-template-columns:
      2fr
      1fr
      1fr
      1fr;
  }

  .saving-time {
    display: none;
  }
}


@media (max-width: 800px) {

  .dashboard {
    padding: 18px;
  }

  .header {
    align-items: flex-start;

    flex-direction: column;

    gap: 18px;
  }

  .summary-grid {
    grid-template-columns: 1fr;
  }

  .insights-grid {
    grid-template-columns: 1fr;
  }

  .savings-status {
    flex-direction: column;

    gap: 10px;
  }

  .anomaly-stats {
    grid-template-columns: 1fr;
  }

  .automation-row {
    grid-template-columns:
      auto
      1fr;
  }

  .automation-power {
    grid-column: 2;
  }

  .automation-time {
    grid-column: 2;
  }

  .saving-row {
    grid-template-columns:
      1fr 1fr;
  }

  .saving-device {
    grid-column: 1 / -1;
  }

  .devices-grid {
    grid-template-columns: 1fr;
  }

  .footer {
    flex-direction: column;

    gap: 6px;
  }
}


@media (max-width: 500px) {

  .dashboard {
    padding: 12px;
  }

  .panel {
    padding: 17px;
  }

  .header h1 {
    font-size: 22px;
  }

  .title-row {
    align-items: flex-start;
  }

  .home-icon {
    width: 46px;
    height: 46px;
  }

  .saving-row {
    grid-template-columns: 1fr;
  }

  .saving-stat {
    display: flex;

    justify-content: space-between;

    align-items: center;
  }

  .saving-stat span {
    margin: 0;
  }

  .automation-power {
    flex-direction: column;

    gap: 8px;
  }

  .automation-power div {
    display: flex;

    justify-content: space-between;

    text-align: left;
  }
}
</style>