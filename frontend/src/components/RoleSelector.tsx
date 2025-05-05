interface Props {
    onSelect: (role: "in-favor" | "against") => void;
  }
  
  export function RoleSelector({ onSelect }: Props) {
    return (
      <div className="flex gap-4 my-4">
        <button onClick={() => onSelect("in-favor")} className="bg-green-500 text-white px-4 py-2 rounded">In Favor</button>
        <button onClick={() => onSelect("against")} className="bg-red-500 text-white px-4 py-2 rounded">Against</button>
      </div>
    );
  }
  