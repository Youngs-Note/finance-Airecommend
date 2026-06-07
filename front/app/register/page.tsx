"use client";
import { register } from "@/app/register/actions";
import Input from "@/components/input";
import Link from "next/link";
import { useActionState } from "react";

export default function Signup() {
  const [state, action] = useActionState(register, null);
  return (
    <main className="flex flex-col min-h-screen bg-gray-50 p-6">
      {/* 상단 뒤로가기 및 헤더 */}
      <header className="flex items-center mb-8 mt-4">
        <Link
          href="/"
          className="text-gray-500 hover:text-gray-900 transition-colors"
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
              d="M15 19l-7-7 7-7"
            />
          </svg>
        </Link>
      </header>

      {/* 안내 문구 영역 */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2 leading-tight">
          조금만 더 알려주시면
          <br />
          <span className="text-green-600">맞춤 금융 상품</span>을 찾아드릴게요!
        </h1>
        <p className="text-sm text-gray-500 mt-2">
          정확한 금리 비교를 위해 필요한 최소한의 정보입니다.
        </p>
      </div>

      {/* 정보 입력 폼 */}
      <form action={action} className="flex-1 flex flex-col space-y-6">
        {/* 아이디 입력 */}
        <div className="flex flex-col space-y-2">
          <label
            htmlFor="userId"
            className="text-sm font-semibold text-gray-700"
          >
            아이디
          </label>
          <Input
            errors={state?.fieldErrors.userId}
            name="userId"
            required
            type="text"
            id="userId"
            placeholder="사용하실 아이디를 입력해주세요"
            minLength={4}
          />
        </div>

        {/* 비밀번호 입력 */}
        <div className="flex flex-col space-y-2">
          <label
            htmlFor="password"
            className="text-sm font-semibold text-gray-700"
          >
            비밀번호
          </label>
          <Input
            errors={state?.fieldErrors.password}
            required
            name="password"
            type="password"
            id="password"
            placeholder="비밀번호를 입력해주세요"
            minLength={8}
          />
        </div>

        {/* 비밀번호 확인 입력 */}
        <div className="flex flex-col space-y-2">
          <label
            htmlFor="passwordConfirm"
            className="text-sm font-semibold text-gray-700"
          >
            비밀번호 확인
          </label>
          <Input
            errors={state?.fieldErrors.passwordConfirm}
            name="passwordConfirm"
            required
            type="password"
            id="passwordConfirm"
            placeholder="비밀번호를 다시 한 번 입력해주세요"
            minLength={8}
          />
        </div>

        {/* 이름 입력 */}
        <div className="flex flex-col space-y-2">
          <label htmlFor="name" className="text-sm font-semibold text-gray-700">
            이름
          </label>
          <Input
            errors={state?.fieldErrors?.userName}
            name="userName"
            required
            type="text"
            id="name"
            placeholder="홍길동"
            minLength={2}
          />
        </div>

        {/* 생년월일 입력 */}
        <div className="flex flex-col space-y-2">
          <label htmlFor="dob" className="text-sm font-semibold text-gray-700">
            생년월일
          </label>
          <Input
            errors={state?.fieldErrors.birth}
            name="birth"
            required
            type="date"
            id="dob"
          />
        </div>

        {/* 이메일 입력 */}
        <div className="flex flex-col space-y-2">
          <label
            htmlFor="email"
            className="text-sm font-semibold text-gray-700"
          >
            이메일
          </label>
          <Input
            errors={state?.fieldErrors.email}
            name="email"
            required
            type="email"
            id="email"
            placeholder="example@finmatch.com"
          />
        </div>

        {/* 하단 여백 (버튼을 아래로 밀어내기 위함) */}
        <div className="flex-1"></div>

        {/* 가입 완료 버튼 */}
        <button
          type="submit"
          className="w-full py-4 mb-4 rounded-xl bg-green-600 text-white font-bold text-base shadow-md hover:bg-green-700 transition-colors"
        >
          입력 완료하고 시작하기
        </button>
      </form>
    </main>
  );
}
