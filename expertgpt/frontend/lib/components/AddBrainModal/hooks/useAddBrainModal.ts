/* eslint-disable max-lines */
import axios from "axios";
import { useState } from "react";  // useEffect
import { useForm } from "react-hook-form";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { usePromptApi } from "@/lib/api/prompt/usePromptApi";
import { useBrainConfig } from "@/lib/context/BrainConfigProvider";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
// import { defineMaxTokens } from "@/lib/helpers/defineMexTokens";
import { useToast } from "@/lib/hooks";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAddBrainModal = () => {
  const [isPending, setIsPending] = useState(false);
  const { publish } = useToast();
  const { createBrain, setActiveBrain } = useBrainContext();
  const { setAsDefaultBrain } = useBrainApi();
  const { createPrompt } = usePromptApi();
  const [isShareModalOpen, setIsShareModalOpen] = useState(false);
  const { config } = useBrainConfig();
  const defaultValues = {
    ...config,
    name: "",
    description: "",
    setDefault: false,
    prompt: {
      title: "",
      content: "",
    },
    linkedin: "",
    openAiKey: "",
    model: "gpt-3.5-turbo-0613",
    temperature: 0.5,
    maxTokens: 256,
    conscientiousness: 0,
    neuroticism: 0,
    extraversion: 0
  };

  const { register, getValues, reset, setValue } = useForm({
    defaultValues,
  }); //watch, 

  // const openAiKey = watch("openAiKey");
  // const model = watch("model");
  // const temperature = watch("temperature");
  // const maxTokens = watch("maxTokens");

  // useEffect(() => {
  //   setValue("maxTokens", Math.min(maxTokens, defineMaxTokens(model)));
  // }, [maxTokens, model, setValue]);

  const getCreatingBrainPromptId = async (): Promise<string | undefined> => {
    const { prompt } = getValues();

    if (prompt.title.trim() !== "" && prompt.content.trim() !== "") {
      return (await createPrompt(prompt)).id;
    }

    return undefined;
  };

  const handleSubmit = async () => {
    const { name, description, linkedin, model, openAiKey, temperature, maxTokens, conscientiousness, neuroticism, extraversion, setDefault } = getValues();

    if (name.trim() === "" || isPending) {
      return;
    }

    try {
      setIsPending(true);

      const prompt_id = await getCreatingBrainPromptId();

      const createdBrainId = await createBrain({
        name,
        description,
        max_tokens: maxTokens,
        model,
        openai_api_key: openAiKey,
        temperature,
        prompt_id,
        linkedin,
        conscientiousness,
        neuroticism,
        extraversion,
      });

      if (createdBrainId === undefined) {
        publish({
          variant: "danger",
          text: "Error occurred while creating a brain",
        });

        return;
      }

      setActiveBrain({
        id: createdBrainId,
        name,
      });

      if (setDefault) {
        await setAsDefaultBrain(createdBrainId);
      }

      setIsShareModalOpen(false);
      reset(defaultValues);
      publish({
        variant: "success",
        text: "AI Clone created successfully",
      });
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 429) {
        publish({
          variant: "danger",
          text: `${JSON.stringify(
            (
              err.response as {
                data: { detail: string };
              }
            ).data.detail
          )}`,
        });

        return;
      }
      publish({
        variant: "danger",
        text: `${JSON.stringify(err)}`,
      });
    } finally {
      setIsPending(false);
    }
  };

  const pickPublicPrompt = ({
    title,
    content,
  }: {
    title: string;
    content: string;
  }): void => {
    setValue("prompt.title", title, {
      shouldDirty: true,
    });
    setValue("prompt.content", content, {
      shouldDirty: true,
    });
  };

  return {
    isShareModalOpen,
    setIsShareModalOpen,
    handleSubmit,
    setValue,
    register,
    // openAiKey,
    // model,
    // temperature,
    // maxTokens,
    isPending,
    pickPublicPrompt,
  };
};
