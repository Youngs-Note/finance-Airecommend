import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 p-6">
      <div className="w-full max-w-sm flex flex-col items-center space-y-10">
        {/* 로고 및 타이틀 영역 */}
        <div className="flex flex-col items-center space-y-4">
          {/* 간단한 SVG 아이콘 (지갑/돈 모양) */}
          <div className="flex h-20 w-20 items-center justify-center rounded-full bg-green-100 text-green-600 shadow-sm">
            <svg
              className="h-10 w-10"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>

          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 tracking-tight">
              AI 금융 비서 <span className="text-green-600">FinMatch</span>
            </h1>
            <p className="mt-2 text-sm text-gray-500">
              데이터 기반으로 나에게 딱 맞는 예적금을 찾아보세요
            </p>
          </div>
        </div>

        {/* 버튼 영역 */}
        <div className="w-full flex flex-col space-y-3">
          {/* 시작하기 버튼 (로그인 페이지로 이동) */}
          <Link
            href="/login"
            className="w-full flex justify-center items-center rounded-xl bg-green-600 px-4 py-4 text-base font-semibold text-white shadow-md hover:bg-green-700 transition-colors"
          >
            시작하기
          </Link>

          {/* 회원가입 버튼 */}
          <Link
            href="/register"
            className="w-full flex justify-center items-center rounded-xl bg-white px-4 py-4 text-base font-medium text-green-700 border-2 border-green-100 hover:bg-green-50 hover:border-green-200 transition-colors"
          >
            회원가입
          </Link>
        </div>
      </div>
    </main>
  );
}
