import { signup } from "@/apis/auth";
import { SignupResponse } from "@/types/auth";
import { RESTYPE } from "@/types/common";
import { setAccessToken, setRefreshToken } from "@/utils/auth";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";

export const useSignup = () => {
  const router = useRouter();
  return useMutation({
    mutationFn: signup,
    onSuccess: (data: RESTYPE<SignupResponse>) => {
      if (data.data.access_token && data.data.refresh_token) {
        setAccessToken(data.data.access_token);
        setRefreshToken(data.data.refresh_token);
        router.push("/signin");
      }
    },
    onError: () => {
      router.push("/signup");
    },
  });
};
