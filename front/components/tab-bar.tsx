"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function TabBar() {
  const pathname = usePathname();

  return (
    <div className="flex justify-center bg-gray-100">
      <nav className="max-w-sm fixed bottom-0 w-full bg-white border-t border-gray-200 px-6 py-3 flex justify-between items-center pb-safe">
        {/* 홈 탭 */}
        <Link
          href="/home"
          className={`flex flex-col items-center space-y-1 transition-colors ${
            pathname === "/home"
              ? "text-green-600"
              : "text-gray-400 hover:text-gray-600"
          }`}
        >
          <svg
            className="w-6 h-6"
            fill={pathname === "/home" ? "currentColor" : "none"}
            stroke={pathname === "/home" ? "none" : "currentColor"}
            strokeWidth={2}
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M11.47 3.841a.75.75 0 0 1 1.06 0l8.99 8.99a.75.75 0 1 1-1.06 1.06L20 13.43V20.5a.5.5 0 0 1-.5.5h-5.25a.75.75 0 0 1-.75-.75V15.5a.25.25 0 0 0-.25-.25h-2.5a.25.25 0 0 0-.25.25v4.75a.75.75 0 0 1-.75.75H4.5a.5.5 0 0 1-.5-.5v-7.07l-.46.46a.75.75 0 1 1-1.06-1.06l8.99-8.99Z"
            />
          </svg>
          <span className="text-[10px] font-semibold">홈</span>
        </Link>

        {/* 비교 탭 */}
        <Link
          href="/compare"
          className={`flex flex-col items-center space-y-1 transition-colors ${
            pathname === "/compare"
              ? "text-green-600"
              : "text-gray-400 hover:text-gray-600"
          }`}
        >
          <svg
            className="w-6 h-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
          </svg>
          <span className="text-[10px] font-medium">비교</span>
        </Link>

        {/* AI 추천 탭 */}
        <Link
          href="/recommend"
          className={`flex flex-col items-center space-y-1 transition-colors ${
            pathname === "/recommend"
              ? "text-green-600"
              : "text-gray-400 hover:text-gray-600"
          }`}
        >
          <svg
            className="w-6 h-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 10V3L4 14h7v7l9-11h-7z"
            />
          </svg>
          <span className="text-[10px] font-medium">AI 추천</span>
        </Link>

        {/* 마이페이지 탭 */}
        <Link
          href="/my"
          className={`flex flex-col items-center space-y-1 transition-colors ${
            pathname === "/my"
              ? "text-green-600"
              : "text-gray-400 hover:text-gray-600"
          }`}
        >
          <svg
            className="w-6 h-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
            />
          </svg>
          <span className="text-[10px] font-medium">마이</span>
        </Link>
      </nav>
    </div>
  );
}
