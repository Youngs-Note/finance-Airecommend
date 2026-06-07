"use client";

import type { RateStats } from "@/lib/backend-api";
import { BarController, BarElement, CategoryScale, Chart, LinearScale } from "chart.js";
import { useEffect, useRef } from "react";

Chart.register(BarController, BarElement, CategoryScale, LinearScale);

export default function RateChart({ stats }: { stats: RateStats[] }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!canvasRef.current || stats.length === 0) return;

    const chart = new Chart(canvasRef.current, {
      type: "bar",
      data: {
        labels: stats.map((item) =>
          item.product_type === "deposit" ? "예금" : "적금",
        ),
        datasets: [
          {
            label: "평균 최고금리 (%)",
            data: stats.map((item) => item.average_highest_rate),
            backgroundColor: ["#16a34a", "#4ade80"],
          },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } },
      },
    });

    return () => chart.destroy();
  }, [stats]);

  return <canvas ref={canvasRef} aria-label="예금 적금 평균 최고금리 차트" />;
}
