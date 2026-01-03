export default function StatusBar({ status, type }) {
  if (!status) return null;

  return (
    <div className={`status show ${type}`}>
      {status}
    </div>
  );
}