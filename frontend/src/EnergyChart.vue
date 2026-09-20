<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import axios from "axios";

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

import { Line } from "vue-chartjs";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
);

const readings = ref([]);
const selectedDevice = ref("all");

let refreshInterval;

const fetchHistory = async () => {
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/api/energy-history/"
    );

    readings.value = response.data;
  } catch (error) {
    console.error(
      "Failed to load energy history:",
      error
    );
  }
};

const devices = computed(() => {
  const names = readings.value.map(
    (reading) => reading.device_name
  );

  return [...new Set(names)];
});

const chartData = computed(() => {
  if (!readings.value.length) {
    return {
      labels: [],
      datasets: [],
    };
  }

  // All devices
  if (selectedDevice.value === "all") {
    const grouped = {};

    readings.value.forEach((reading) => {
      // Round timestamp to the nearest second.
      // This groups readings from the simulator
      // that were generated in the same cycle.
      const date = new Date(reading.timestamp);

      date.setMilliseconds(0);

      const timestamp = date.toISOString();

      if (!grouped[timestamp]) {
        grouped[timestamp] = 0;
      }

      grouped[timestamp] += Number(
        reading.power_watts
      );
    });

    const points = Object.entries(grouped);

    return {
      labels: points.map(
        ([timestamp]) =>
          new Date(timestamp).toLocaleTimeString(
            [],
            {
              hour: "2-digit",
              minute: "2-digit",
              second: "2-digit",
            }
          )
      ),

      datasets: [
        {
          label: "Total Household Power",
          data: points.map(
            ([, power]) => power
          ),

          borderColor: "#38bdf8",
          backgroundColor: "rgba(56, 189, 248, 0.15)",

          tension: 0.3,
          pointRadius: 3,
          pointBackgroundColor: "#38bdf8",
          pointBorderColor: "#ffffff",
          pointBorderWidth: 1,

          fill: true,
        },
      ],
    };
  }

  // Individual device
  const filtered = readings.value.filter(
    (reading) =>
      reading.device_name ===
      selectedDevice.value
  );

  return {
    labels: filtered.map(
      (reading) =>
        new Date(
          reading.timestamp
        ).toLocaleTimeString(
          [],
          {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
          }
        )
    ),

    datasets: [
      {
        label: selectedDevice.value,

        data: filtered.map(
          (reading) =>
            Number(
              reading.power_watts
            )
        ),

        borderColor: "#38bdf8",
        backgroundColor: "rgba(56, 189, 248, 0.15)",

        tension: 0.3,
        pointRadius: 3,
        pointBackgroundColor: "#38bdf8",
        pointBorderColor: "#ffffff",
        pointBorderWidth: 1,

        fill: true,
      },
    ],
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,

  plugins: {
    legend: {
      display: true,

      labels: {
        color: "#e2e8f0",
      },
    },

    tooltip: {
      backgroundColor: "#0f172a",
      titleColor: "#f8fafc",
      bodyColor: "#cbd5e1",
      borderColor: "#334155",
      borderWidth: 1,
    },
  },

  scales: {
    y: {
      beginAtZero: true,

      title: {
        display: true,
        text: "Power (W)",
        color: "#94a3b8",
      },

      ticks: {
        color: "#94a3b8",
      },

      grid: {
        color: "rgba(148, 163, 184, 0.15)",
      },
    },

    x: {
      title: {
        display: true,
        text: "Time",
        color: "#94a3b8",
      },

      ticks: {
        color: "#94a3b8",
      },

      grid: {
        color: "rgba(148, 163, 184, 0.08)",
      },
    },
  },
};

onMounted(() => {
  fetchHistory();

  refreshInterval = setInterval(
    fetchHistory,
    5000
  );
});

onUnmounted(() => {
  clearInterval(refreshInterval);
});
</script>

<template>
  <div class="energy-chart">

    <div class="chart-controls">

      <label for="device-select">
        Device
      </label>

      <select
        id="device-select"
        v-model="selectedDevice"
      >

        <option value="all">
          All Devices
        </option>

        <option
          v-for="device in devices"
          :key="device"
          :value="device"
        >
          {{ device }}
        </option>

      </select>

    </div>

    <div class="chart-container">

      <Line
        v-if="readings.length"
        :data="chartData"
        :options="chartOptions"
      />

      <p
        v-else
        class="loading"
      >
        Loading energy data...
      </p>

    </div>

  </div>
</template>

<style scoped>

.energy-chart {
  height: 100%;
}

.chart-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
}

.chart-controls label {
  color: #94a3b8;
  font-size: 14px;
}

.chart-controls select {
  background: #0f172a;
  color: #f8fafc;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 14px;
  cursor: pointer;
}

.chart-controls select:focus {
  outline: none;
  border-color: #38bdf8;
}

.chart-container {
  position: relative;
  height: 320px;
  width: 100%;
}

.loading {
  text-align: center;
  color: #94a3b8;
  padding-top: 120px;
}

</style>