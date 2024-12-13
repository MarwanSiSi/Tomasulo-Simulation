// Helper function to create empty arithmetic station
export const createEmptyArithmeticStation = () => ({
  busy: false,
  op: null,
  vj: null,
  vk: null,
  qj: null,
  qk: null,
  address: null,
});

// Helper function to create empty store station
export const createEmptyStoreStation = () => ({
  busy: false,
  address: null,
  v: null,
  q: null,
});

// Helper function to create empty load station
export const createEmptyLoadStation = () => ({
  busy: false,
  address: null,
});

// Helper function to create stations dynamically
export const createStations = (prefix, size, createEmptyStation) => {
  return Array(size)
    .fill()
    .reduce(
      (acc, _, idx) => ({
        ...acc,
        [`${prefix}${idx + 1}`]: createEmptyStation(),
      }),
      {}
    );
};
