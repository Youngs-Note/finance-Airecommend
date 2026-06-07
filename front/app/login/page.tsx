"use client"; // 클라이언트 컴포넌트로 변경 (NextAuth signIn 함수 등을 사용하기 위함)

import { signIn } from "next-auth/react";
import Link from "next/link";
import { useState } from "react";

export default function Login() {
  const [errorMessage, setErrorMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrorMessage("");
    setIsSubmitting(true);

    const formData = new FormData(e.currentTarget);
    const userId = formData.get("userId");
    const password = formData.get("password");

    try {
      const result = await signIn("credentials", {
        userId,
        password,
        redirect: false,
      });

      if (!result?.ok) {
        setErrorMessage("아이디 또는 비밀번호가 일치하지 않습니다.");
        return;
      }

      window.location.assign("/home");
    } catch {
      setErrorMessage("아이디 또는 비밀번호가 일치하지 않습니다.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 p-6">
      {/* 로그인 카드 컨테이너 */}
      <div className="w-full max-w-sm flex flex-col items-center bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
        {/* 타이틀 영역 */}
        <div className="flex flex-col items-center space-y-2 text-center w-full mb-8">
          <h1 className="text-2xl font-bold text-gray-900">환영합니다!</h1>
          <p className="text-sm text-gray-500">
            FinMatch의 AI 금융 비서를 만나보세요
          </p>
        </div>

        {/* 이메일/비밀번호 폼 영역 */}
        <form onSubmit={handleSubmit} className="w-full space-y-4">
          <div>
            <label
              htmlFor="userId"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              아이디
            </label>
            <input
              type="text"
              id="userId"
              name="userId"
              placeholder="아이디 입력해주세요"
              required
              className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-sm"
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              비밀번호
            </label>
            <input
              type="password"
              id="password"
              name="password"
              placeholder="비밀번호를 입력해주세요"
              required
              className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-sm"
            />
          </div>

          {/* 에러 메시지 출력 영역 */}
          {errorMessage && (
            <p className="text-red-500 text-xs text-center">{errorMessage}</p>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className="h-10 w-full mt-5 flex items-center justify-center rounded-xl bg-green-600 px-4 py-4 text-base font-semibold text-white shadow-sm hover:bg-green-700 transition-colors"
          >
            {isSubmitting ? "로그인 중..." : "로그인"}
          </button>
        </form>

        {/* 회원가입 유도 링크 */}
        <div className="mt-6 text-sm text-gray-500">
          계정이 없으신가요?{" "}
          <Link
            href="/register"
            className="text-green-600 font-semibold hover:underline"
          >
            회원가입
          </Link>
        </div>

        {/* 안내 문구 및 약관 */}
        <div className="text-center text-xs text-gray-400 mt-8">
          로그인 시 FinMatch의{" "}
          <Link href="#" className="underline hover:text-gray-600">
            이용약관
          </Link>{" "}
          및 <br />
          <Link href="#" className="underline hover:text-gray-600">
            개인정보처리방침
          </Link>
          에 동의하게 됩니다.
        </div>
      </div>

      {/* 뒤로가기 링크 */}
      <div className="mt-8">
        <Link
          href="/"
          className="text-sm text-gray-400 hover:text-gray-600 underline underline-offset-4 transition-colors"
        >
          홈으로 돌아가기
        </Link>
      </div>
    </main>
  );
}
