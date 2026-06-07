"use client";

import Input from "@/components/input";
import Link from "next/link";

export default function ChangePasswordPage() {
  return (
    <main className="flex min-h-screen flex-col bg-gray-50 p-6">
      <header className="mb-8 mt-4 flex items-center">
        <Link
          href="/my"
          className="text-gray-500 transition-colors hover:text-gray-900"
        >
          <svg
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 19l-7-7 7-7"
            />
          </svg>
        </Link>
        <h1 className="ml-4 text-xl font-bold text-gray-900">비밀번호 변경</h1>
      </header>

      <div className="flex flex-1 flex-col space-y-6">
        <p className="rounded-xl bg-amber-50 p-4 text-sm text-amber-800">
          비밀번호 변경 기능은 준비 중입니다.
        </p>

        <Input
          name="currentPassword"
          id="currentPassword"
          type="password"
          placeholder="현재 비밀번호"
          disabled
        />
        <Input
          name="newPassword"
          id="newPassword"
          type="password"
          placeholder="새 비밀번호"
          disabled
        />
        <Input
          name="confirmPassword"
          id="confirmPassword"
          type="password"
          placeholder="새 비밀번호 확인"
          disabled
        />

        <button
          type="button"
          disabled
          className="mb-4 w-full rounded-xl bg-gray-400 py-4 text-base font-bold text-white"
        >
          준비 중
        </button>
      </div>
    </main>
  );
}
