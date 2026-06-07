export default function Loading() {
  return (
    // 레이아웃 중앙에 배치하기 위한 flex 컨테이너
    <div className="flex flex-col items-center justify-center flex-1 h-full min-h-[60vh] space-y-4">
      {/* 회전하는 스피너 (Spinning Circle) */}
      <div className="w-12 h-12 rounded-full border-4 border-gray-100 border-t-green-600 animate-spin"></div>
    </div>
  );
}
