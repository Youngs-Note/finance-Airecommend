"use client";

import Input from "@/components/input";
import { useSession } from "next-auth/react";
import Link from "next/link";

export default function ChangeInfo() {
  const { data: session, status } = useSession();

  if (status === "loading") {
    return (
      <main className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-green-600"></div>
      </main>
    );
  }

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
        <h1 className="ml-4 text-xl font-bold text-gray-900">내 정보 수정</h1>
      </header>

      <div className="flex flex-1 flex-col space-y-6">
        <p className="rounded-xl bg-amber-50 p-4 text-sm text-amber-800">
          내 정보 수정 기능은 준비 중입니다. 현재 등록 정보를 확인할 수 있습니다.
        </p>

        <div className="flex flex-col space-y-2">
          <label htmlFor="userName" className="text-sm font-semibold text-gray-700">
            이름
          </label>
          <Input
            name="userName"
            id="userName"
            type="text"
            value={session?.user?.name || ""}
            readOnly
            disabled
          />
        </div>

        <div className="flex flex-col space-y-2">
          <label htmlFor="email" className="text-sm font-semibold text-gray-700">
            이메일
          </label>
          <Input
            name="email"
            id="email"
            type="email"
            value={session?.user?.email || ""}
            readOnly
            disabled
          />
        </div>

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
