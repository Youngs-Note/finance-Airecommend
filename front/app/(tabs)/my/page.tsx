import { authOptions } from "@/lib/auth";
import { getServerSession } from "next-auth";
import Link from "next/link";
import LogoutButton from "../../../components/LogoutButton";

export default async function MyPage() {
  const session = await getServerSession(authOptions);
  const userName = session?.user?.name || "회원";
  const userEmail = session?.user?.email || "이메일 정보가 없습니다";

  return (
    <main className="relative bg-gray-50 flex flex-col min-h-screen">
      {/* 상단 헤더 영역 */}
      <header className="px-6 pt-5 pb-4 bg-white rounded-b-3xl shadow-sm z-10">
        <h1 className="text-xl font-bold text-gray-900">마이페이지</h1>
      </header>

      {/* 메인 콘텐츠 영역 (하단 탭바 높이만큼 여백 pb-24 부여) */}
      <div className="flex-1 px-6 py-6 overflow-y-auto pb-24 space-y-6">
        {/* 프로필 섹션 */}
        <section className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center space-x-4">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-bold text-xl">
            {userName.charAt(0)}
          </div>
          <div>
            <h2 className="text-lg font-bold text-gray-900">{userName}님</h2>
            <p className="text-sm text-gray-500">{userEmail}</p>
          </div>
        </section>

        {/* 설정 메뉴 섹션 */}
        <section className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <h3 className="text-sm font-bold text-gray-800 px-6 py-4 border-b border-gray-50">
            회원 정보 관리
          </h3>
          <ul className="divide-y divide-gray-50">
            <li>
              <Link
                href="/my/changeInfo"
                className="flex items-center justify-between px-6 py-4 hover:bg-gray-50 transition-colors"
              >
                <span className="text-gray-700">이메일 및 내 정보 수정</span>
                <span className="text-gray-400">
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </span>
              </Link>
            </li>
            <li>
              <Link
                href="/my/changePassword"
                className="flex items-center justify-between px-6 py-4 hover:bg-gray-50 transition-colors"
              >
                <span className="text-gray-700">비밀번호 변경</span>
                <span className="text-gray-400">
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </span>
              </Link>
            </li>
          </ul>
        </section>

        {/* 로그아웃 섹션 */}
        <section className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <LogoutButton />
        </section>
      </div>
    </main>
  );
}
