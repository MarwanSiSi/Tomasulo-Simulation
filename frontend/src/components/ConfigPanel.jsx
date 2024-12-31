import PropTypes from "prop-types";
import axios from "axios";

const ConfigPanel = ({ config, setConfig }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setConfig((prev) => ({
      ...prev,
      [name]: parseInt(value),
    }));
  };

  const handleSubmit = async () => {
    axios.post("http://0.0.0.0:8080/config", config);
  };

  return (
    <div className="mb-8 p-4 bg-gray-50 rounded-lg">
      <h2 className="text-2xl font-bold">Configuration</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 divide-y-2 divide-black">
        {/* Latency Configuration */}
        <div className="lg:col-span-4 my-4">
          <h3 className="font-semibold text-xl underline my-5">
            Latency Configuration
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label className="block text-base font-medium mb-1">
                Float Add/Sub Latency
              </label>
              <input
                type="number"
                name="floatAddSubLatency"
                value={config.floatAddSubLatency}
                onChange={handleChange}
                min="1"
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-base font-medium mb-1">
                Float Mul/Div Latency
              </label>
              <input
                type="number"
                name="floatMulDivLatency"
                value={config.floatMulDivLatency}
                onChange={handleChange}
                min="1"
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-base font-medium mb-1">
                Int Add/Sub Latency
              </label>
              <input
                type="number"
                name="intAddSubLatency"
                value={config.intAddSubLatency}
                onChange={handleChange}
                min="1"
                className="w-full p-2 border rounded"
              />
            </div>
          </div>
        </div>

        {/* Station Size Configuration */}
        <div className="lg:col-span-4 my-4">
          <h3 className="font-semibold my-5 text-xl underline">
            Station Size Configuration
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label className="block text-base font-medium mb-1">
                Load Buffer Size
              </label>
              <input
                type="number"
                name="loadBufferSize"
                value={config.loadBufferSize}
                onChange={handleChange}
                min="1"
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-base font-medium mb-1">
                Store Buffer Size
              </label>
              <input
                type="number"
                name="storeBufferSize"
                value={config.storeBufferSize}
                onChange={handleChange}
                min="1"
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-base font-medium mb-1">
                Float Add/Sub Station Size
              </label>
              <input
                type="number"
                name="floatAddSubStationSize"
                value={config.floatAddSubStationSize}
                onChange={handleChange}
                min="1"
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-base font-medium mb-1">
                Float Mul/Div Station Size
              </label>
              <input
                type="number"
                name="floatMulDivStationSize"
                value={config.floatMulDivStationSize}
                onChange={handleChange}
                min="1"
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-base font-medium mb-1">
                Int Add/Sub Station Size
              </label>
              <input
                type="number"
                name="intAddSubStationSize"
                value={config.intAddSubStationSize}
                onChange={handleChange}
                min="1"
                className="w-full p-2 border rounded"
              />
            </div>
          </div>
        </div>

        {/* Cache Configuration */}
        <div className="lg:col-span-4 mt-4">
          <h3 className="font-semibold my-5 underline text-xl">
            Cache Configuration
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label className="block text-base font-medium mb-1">
                Cache Hit Latency
              </label>
              <input
                type="number"
                name="cacheHitLatency"
                value={config.cacheHitLatency}
                onChange={handleChange}
                min="1"
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-base font-medium mb-1">
                Cache Miss Latency
              </label>
              <input
                type="number"
                name="cacheMissLatency"
                value={config.cacheMissLatency}
                onChange={handleChange}
                min="1"
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-base font-medium mb-1">
                Cache Size (bytes)
              </label>
              <input
                type="number"
                name="cacheSize"
                value={config.cacheSize}
                onChange={handleChange}
                min="1"
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-base font-medium mb-1">
                Block Size (bytes)
              </label>
              <input
                type="number"
                name="blockSize"
                value={config.blockSize}
                onChange={handleChange}
                min="1"
                className="w-full p-2 border rounded"
              />
            </div>
            <button
              onClick={handleSubmit}
              className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
            >
              Submit Configuration
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

ConfigPanel.propTypes = {
  config: PropTypes.shape({
    // Latency configuration
    floatAddSubLatency: PropTypes.number.isRequired,
    floatMulDivLatency: PropTypes.number.isRequired,
    intAddSubLatency: PropTypes.number.isRequired,

    // Station size configuration
    loadBufferSize: PropTypes.number.isRequired,
    storeBufferSize: PropTypes.number.isRequired,
    floatAddSubStationSize: PropTypes.number.isRequired,
    floatMulDivStationSize: PropTypes.number.isRequired,
    intAddSubStationSize: PropTypes.number.isRequired,

    // Cache configuration
    cacheHitLatency: PropTypes.number.isRequired,
    cacheMissLatency: PropTypes.number.isRequired,
    cacheSize: PropTypes.number.isRequired,
    blockSize: PropTypes.number.isRequired,
  }).isRequired,
  setConfig: PropTypes.func.isRequired,
};

export default ConfigPanel;
