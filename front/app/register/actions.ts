"use server";

import { prisma } from "@/lib/prisma";
import bcrypt from "bcryptjs";
import { redirect } from "next/navigation";
import { z } from "zod";

const formSchema = z
  .object({
    userId: z.string().min(4, { message: "아이디는 4자 이상이어야 합니다." }),
    userName: z.string().min(2, { message: "이름은 2자 이상이어야 합니다." }),
    email: z.email({ message: "유효한 이메일 주소를 입력해주세요." }).trim(),
    birth: z.coerce.date({ message: "생년월일을 입력해주세요." }),
    password: z
      .string()
      .min(8, { message: "비밀번호는 8자 이상이어야 합니다." }),
    passwordConfirm: z
      .string()
      .min(8, { message: "비밀번호는 8자 이상이어야 합니다." }),
  })
  .refine((data) => data.password === data.passwordConfirm, {
    message: "비밀번호가 일치하지 않습니다",
    path: ["passwordConfirm"],
  });

// 매개변수 순서 변경: prevState가 먼저 와야 합니다.
export async function register(_prevState: unknown, formData: FormData) {
  const data = {
    userId: formData.get("userId"),
    userName: formData.get("userName"),
    email: formData.get("email"),
    birth: formData.get("birth"),
    password: formData.get("password"),
    passwordConfirm: formData.get("passwordConfirm"),
  };

  const result = formSchema.safeParse(data);

  if (!result.success) {
    const flatten = z.flattenError(result.error);
    return { fieldErrors: flatten.fieldErrors };
  }

  try {
    const { userId, userName, email, birth, password } = result.data;

    const hashedPassword = await bcrypt.hash(password, 10);

    await prisma.user.create({
      data: {
        userId: userId,
        name: userName,
        email: email,
        birth: birth,
        password: hashedPassword,
      },
    });
  } catch (error) {
    console.error("회원가입 에러:", error);
    return { fieldErrors: { email: ["이미 존재하는 이메일 입니다."] } };
  }

  redirect("/login");
}
