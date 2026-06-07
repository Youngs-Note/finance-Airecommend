import { InputHTMLAttributes } from "react";

interface IInputProps {
  errors?: string[];
  name: string;
}

export default function FormInput({
  errors = [],
  name,
  ...rest
}: IInputProps & InputHTMLAttributes<HTMLInputElement>) {
  return (
    <div className="flex flex-col gap-2">
      <input
        name={name}
        className={`w-full px-4 py-3 rounded-xl border bg-white focus:outline-none focus:ring-2 focus:border-transparent transition-all ${
          errors.length > 0
            ? "border-red-500 ring-2 ring-red-500 focus:ring-red-500"
            : "border-gray-200 focus:invalid:ring-red-500 focus:valid:ring-green-500"
        }`}
        {...rest}
      />
      {errors.map((error, index) => (
        <span key={index} className="text-red-500 font-medium">
          {error}
        </span>
      ))}
    </div>
  );
}
