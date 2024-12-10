import PropTypes from "prop-types";

const ConfigPanel = ({ config, setConfig }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setConfig((prev) => ({
      ...prev,
      [name]: parseInt(value),
    }));
  };
  console.log(config);

  return (
    <div className="mb-8 p-4 bg-gray-50 rounded-lg">
      <h2 className="text-xl font-bold mb-4">Configuration</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Add Latency</label>
          <input
            type="number"
            name="addLatency"
            value={config.addLatency}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Sub Latency</label>
          <input
            type="number"
            name="subLatency"
            value={config.subLatency}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Mul Latency</label>
          <input
            type="number"
            name="mulLatency"
            value={config.mulLatency}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Div Latency</label>
          <input
            type="number"
            name="divLatency"
            value={config.divLatency}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Load Latency</label>
          <input
            type="number"
            name="loadLatency"
            value={config.loadLatency}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">
            Store Latency
          </label>
          <input
            type="number"
            name="storeLatency"
            value={config.storeLatency}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">
            Cache Size (bytes)
          </label>
          <input
            type="number"
            name="cacheSize"
            value={config.cacheSize}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">
            Block Size (bytes)
          </label>
          <input
            type="number"
            name="blockSize"
            value={config.blockSize}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
        </div>
      </div>
    </div>
  );
};

export default ConfigPanel;

ConfigPanel.propTypes = {
  config: PropTypes.shape({
    addLatency: PropTypes.number.isRequired,
    subLatency: PropTypes.number.isRequired,
    mulLatency: PropTypes.number.isRequired,
    divLatency: PropTypes.number.isRequired,
    loadLatency: PropTypes.number.isRequired,
    storeLatency: PropTypes.number.isRequired,
    cacheSize: PropTypes.number.isRequired,
    blockSize: PropTypes.number.isRequired,
  }).isRequired,
  setConfig: PropTypes.func.isRequired,
};
