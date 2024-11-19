import { useEffect, useState, useRef } from "react";
import "./OutputTextComponent.css";

interface Props {
  text: string;
}

const OutputTextComponent = ({ text }: Props) => {
  const [displayedText, setDisplayedText] = useState<string>("");
  const indexRef = useRef(0);

  useEffect(() => {
    indexRef.current = 0;
    setDisplayedText("");

    const interval = setInterval(() => {
      if (indexRef.current < text.length) {
        setDisplayedText((prev) => prev + text.charAt(indexRef.current));
        indexRef.current += 1;
      } else {
        clearInterval(interval);
      }
    }, 100);

    return () => clearInterval(interval);
  }, [text]);

  return (
    <div className="output-text-container">
      <p>{displayedText || "Your generated text will appear here."}</p>
    </div>
  );
};

export default OutputTextComponent;
