import Image from "next/image";
import Link from "next/link";

export const Logo = (): JSX.Element => {
  return (
    <Link href={"/"} className="flex items-center gap-4">
      <Image
        className="full"
        src={"/logo.svg"}
        alt="ExpertGPT logo"
        width={48}
        height={48}
      />
      <h1 className="font-bold">ExpertGPT</h1>
    </Link>
  );
};
