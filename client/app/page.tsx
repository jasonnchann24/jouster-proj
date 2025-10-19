"use client";
import Image from "next/image";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

import { Separator } from "@/components/ui/separator";

import { Textarea } from "@/components/ui/textarea";
import { Spinner } from "@/components/ui/spinner";
import { Button } from "@/components/ui/button";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useEffect, useMemo, useState } from "react";

export default function Home() {
  const baseUrl = "http://localhost:8000";
  const [value, setValue] = useState("");

  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      if (value.trim() === "") {
        return;
      }

      const response = await fetch(`${baseUrl}/analyze/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: value }),
        credentials: "include",
      });

      if (!response.ok) {
        console.error("Error submitting text for analysis");
        return;
      }

      const data = await response.json();
      // unshift the new analysis result to recentAnalysis.results
      setRecentAnalysis((prev) => ({
        ...prev,
        results: [data, ...prev.results],
      }));

      console.log(data);
    } finally {
      setTimeout(() => {
        setIsLoading(false);
      }, 1000);
    }
  };

  const [isListLoading, setIsListLoading] = useState(false);
  type Result = {
    id: number;
    user_id: number | null;
    text: string;
    summarized_text: string;
    extracted_metadata: {
      title: string;
      topics: string[];
      sentiment: string;
      keywords: string[];
    };
    user: any | null;
    created_at: string;
  };
  type AnalysisResult = {
    count: number;
    next: string;
    previous: string;
    results: Array<Result>;
  };

  const [recentAnalysis, setRecentAnalysis] = useState<AnalysisResult>({
    count: 0,
    next: "",
    previous: "",
    results: [],
  });
  const analysis = useMemo(() => {
    return recentAnalysis?.results || [];
  }, [recentAnalysis]);

  const [search, setSearch] = useState("");

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      getList();
    }, 500);

    return () => clearTimeout(delayDebounceFn);
  }, [search]);

  useEffect(() => {
    getList();
  }, []);

  const getList = async () => {
    setIsListLoading(true);
    try {
      let url = `${baseUrl}/search/`;
      if (search.trim() !== "") {
        url += `?topics=${encodeURIComponent(search.trim())}`;
      }
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });

      if (!response.ok) {
        console.error("Error fetching recent analysis");
        return;
      }

      const data = await response.json();
      setRecentAnalysis(data);
      console.log(data);
    } finally {
      setIsListLoading(false);
    }
  }

  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start w-2/5 mx-auto">
        <h1 className="text-3xl">Text Analyzer - Jouster</h1>
        <ol className="font-mono list-inside list-decimal text-sm/6 text-center sm:text-left">
          <li className="mb-2 tracking-[-.01em]">Supply your text here</li>
          <li className="tracking-[-.01em]">Submit for analysis</li>
        </ol>
        <Textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Type your message here."
          rows={30}
          disabled={isLoading}
        />

        <div className="w-full">
          <Button
            variant="outline"
            onClick={handleSubmit}
            disabled={isLoading}
            className="cursor-pointer w-full hover:bg-white/10"
          >
            Submit
            {isLoading && <Spinner />}
          </Button>
        </div>
        <Separator className="bg-blue-500" />

        <div className="w-full">
          <Card className="w-full">
            <CardHeader>
              <CardTitle>Recent Analysis</CardTitle>
              <CardDescription>
                Here are the most recent analysis results.
              </CardDescription>
              <CardAction>
                <Input type="text" placeholder="Topic search ..." value={search} onChange={(e) => setSearch(e.target.value)} />
              </CardAction>
            </CardHeader>
            <CardContent>
              <Accordion
                type="single"
                collapsible
                className="w-full"
                defaultValue="item-1"
              >
                {analysis.map((item, idx) => (
                  <AccordionItem value={`item-${item.id}`} key={item.id}>
                    <AccordionTrigger><span><b>Title:</b> {`${item.extracted_metadata.title}`}</span></AccordionTrigger>
                    <AccordionContent className="flex flex-col gap-4 text-balance">
                      <p>
                        <b className="text-blue-400">Summary:</b> {item.summarized_text}
                      </p>
                      <p>
                        <b className="text-blue-400">Sentiment:</b> {item.extracted_metadata.sentiment}
                      </p>
                      <div>
                        <b className="text-blue-400">Keywords:</b>
                        <ul className="list-disc ml-6">
                          {item.extracted_metadata.keywords.map((keyword, kIdx) => (
                            <li key={`item-${item.id}-keyword-${kIdx}`}>{keyword}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <b className="text-blue-400">Topics:</b>
                        <ul className="list-disc ml-6">
                          {item.extracted_metadata.topics.map((keyword, kIdx) => (
                            <li key={`item-${item.id}-topics-${kIdx}`}>{keyword}</li>
                          ))}
                        </ul>
                      </div>
                      <p><b className="text-blue-400">Original Text:</b> <br/>{item.text.split('\n').map((line, idx) => (
                        <span key={`item-${item.id}-line-${idx}`}>
                          {line}
                          <br />
                        </span>
                      ))}</p>
                      <p><b className="text-blue-400">Created at:</b> {new Date(item.created_at).toLocaleString()}</p>
                    </AccordionContent>
                  </AccordionItem>
                ))}

              </Accordion>
            </CardContent>

          </Card>
        </div>
      </main>
    </div>
  );
}
