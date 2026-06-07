import { getToken } from "next-auth/jwt";
import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

interface Routes {
  [key: string]: boolean;
}

const publicOnlyUrls: Routes = {
  "/": true,
  "/login": true,
  "/register": true,
};

export async function proxy(req: NextRequest) {
  // 1. 현재 사용자의 로그인 토큰(세션)을 확인합니다.
  const token = await getToken({
    req,
    secret: process.env.NEXTAUTH_SECRET,
  });

  // 2. 로그인된 상태에서 접근하면 안 되는 페이지 목록
  const exists = publicOnlyUrls[req.nextUrl.pathname];
  if (token) {
    if (exists) {
      return NextResponse.redirect(new URL("/home", req.url));
    }
  } else {
    if (!exists) {
      // 토큰(세션)이 있는데 auth 페이지에 접근하려고 하면 /home으로 쫓아냅니다.
      return NextResponse.redirect(new URL("/login", req.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
