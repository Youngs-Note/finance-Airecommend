import AuthProvider from "@/components/AuthProvider";
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "FinMatch - AI 금융 비서", // 탭 이름도 서비스에 맞게 바꿔보세요!
  description: "AI 기반 금융상품(예적금) 비교 및 맞춤 추천 서비스",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="ko" // 한국어 서비스이므로 en에서 ko로 변경하는 것이 좋습니다.
      className={`${geistSans.variable} ${geistMono.variable} antialiased`}
    >
      {/* 1. 데스크톱 배경 영역 (회색 바탕, 가운데 정렬) */}
      <body className="bg-gray-100 flex justify-center min-h-screen">
        {/* 2. 모바일 앱 화면 프레임 (최대 너비 고정, 흰색 배경, 그림자) */}
        <div className="relative w-full max-w-sm min-h-screen bg-white  flex flex-col">
          {/* 실제 페이지 내용(page.tsx)이 렌더링되는 곳 */}
          <div className="flex-1 overflow-x-hidden flex flex-col">
            <AuthProvider>{children}</AuthProvider>
          </div>
        </div>
      </body>
    </html>
  );
}
