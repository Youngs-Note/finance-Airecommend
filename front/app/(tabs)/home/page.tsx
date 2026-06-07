import { authOptions } from "@/lib/auth";
import { getServerSession } from "next-auth";
import Link from "next/link";

export default async function HomeDashboard() {
  const session = await getServerSession(authOptions);
  const userName = session?.user?.name || "회원";

  return (
    <main className="relative flex min-h-screen flex-col bg-gray-50">
      <header className="z-10 rounded-b-3xl bg-white px-6 pb-4 pt-5 shadow-sm">
        <h1 className="text-xl font-bold text-gray-900">
          반갑습니다, <span className="text-green-600">{userName}</span>님
        </h1>
      </header>

      <div className="flex-1 space-y-6 overflow-y-auto px-6 py-6 pb-24">
        <section className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-green-500 to-green-600 p-6 text-white shadow-md">
          <div className="relative z-10">
            <span className="mb-3 inline-block rounded-md bg-white/20 px-2 py-1 text-xl font-semibold">
              맞춤 추천
            </span>
            <h2 className="mb-1 text-lg font-bold">입력 조건으로 살펴보는</h2>
            <h2 className="mb-4 text-lg font-bold">우선 확인 상품</h2>
            <Link
              href="/recommend"
              className="inline-block rounded-xl bg-white px-4 py-2 text-sm font-semibold text-green-600 shadow-sm transition-colors hover:bg-green-50"
            >
              추천 확인하기
            </Link>
          </div>
          <div className="absolute -bottom-6 -right-6 h-32 w-32 rounded-full bg-white/10 blur-2xl"></div>
        </section>

        <section className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
          <h3 className="mb-2 font-bold text-gray-800">공식 상품 비교</h3>
          <p className="text-sm leading-relaxed text-gray-500">
            금융감독원 금융상품 정보를 기준으로 예금과 적금을 확인하고 비교할 수
            있습니다.
          </p>
          <Link
            href="/compare"
            className="mt-4 inline-block rounded-xl bg-green-50 px-4 py-2 text-sm font-semibold text-green-700"
          >
            상품 비교하기
          </Link>
        </section>
      </div>
    </main>
  );
}
