import { useEffect, useState } from "react";
import "./OutputTextComponent.css";

interface Props {
  text: string;
}

const OutputTextComponent = ({ text }: Props) => {
  const [displayedText, setDisplayedText] = useState<string>("");

  useEffect(() => {
    let index = 0;
    setDisplayedText("");

    const interval = setInterval(() => {
      if (index < text.length) {
        setDisplayedText((prev) => prev + text.charAt(index));
        index++;
      } else {
        clearInterval(interval);
      }
    }, 50);

    return () => clearInterval(interval);
  }, [text]);

  return (
    <div className="output-text-container">
      <p>{displayedText || "Your generated text will appear here."}</p>
    </div>
  );
};

export default OutputTextComponent;
