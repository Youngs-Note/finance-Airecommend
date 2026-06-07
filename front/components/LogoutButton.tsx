"use client";

import { signOut } from "next-auth/react";

export default function LogoutButton() {
  return (
    <button
      onClick={() => signOut({ callbackUrl: "/login" })}
      className="w-full text-left px-6 py-4 text-red-600 font-semibold hover:bg-red-50 transition-colors"
    >
      로그아웃
    </button>
  );
}
