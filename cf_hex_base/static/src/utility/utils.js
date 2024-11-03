/** @odoo-module **/
export const POSITION = {
    "X": [0, 0, 18.75, 18.75, 0, -18.75, -18.75, 0, 18.75, 37.5, 37.5, 37.5, 18.75, 0, -18.75, -37.5, -37.5, -37.5, -18.75,0, 18.75, 37.5, 56.25, 56.25, 56.25,	56.25, 37.5, 18.75,	0, -18.75, -37.5, -56.25, -56.25, -56.25, -56.25, -37.5, -18.75],
    "Y": [0, -20, -10, 10, 20, 10, -10, -40, -30, -20, 0, 20, 30, 40, 30, 20, 0, -20, -30, -60,	-50, -40, -30, -10, 10,	30,	40,	50,	60,	50,	40,	30,	10,	-10, -30, -40, -50,]
};

export const POSITION_V2 = {
//    "X": [16.50, 38.83, 61.16, 83.50, 16.50, 38.83, 61.16, 83.50, 16.50, 38.83, 61.16, 83.50, 16.50, 38.83, 61.16, 83.50,],
//    "Y": [13.75, 23.75, 13.75, 23.75, 34.25, 44.75, 34.25, 44.75, 55.25, 65.75, 55.25, 65.75, 76.25, 86.75, 76.25, 86.75]
    "X": [15.00, 38.33, 61.66, 85.00, 15.00, 38.33, 61.66, 85.00, 15.00, 38.33, 61.66, 85.00, 15.00, 38.33, 61.66, 85.00,],
    "Y": [11.11, 22.22, 11.11, 22.22, 33.33, 44.44, 33.33, 44.44, 55.55, 66.66, 55.55, 66.66, 77.77, 88.88, 77.77, 88.88]
};


export function getAxesV1(index, REDUCTION=0.95) {
    // REDUCTION is a constant used to bring the HEX closer to the center of the QUADRANT.
    // In this way we have the perception that the padding of the QUADRANTS increases
    const asse_y = 50 + POSITION.Y[index - 1] * REDUCTION + "%";
    const asse_x = 50 + POSITION.X[index - 1] * REDUCTION + "%";
    return `top: ${asse_y}; left: ${asse_x};`
}

export function getAxesV2(row, col) {
    // REDUCTION is a constant used to bring the HEX closer to the center of the QUADRANT.
    // In this way we have the perception that the padding of the QUADRANTS increases
    const index = row * 4 + col;
    const asse_y = POSITION_V2.Y[index] + "%";
    const asse_x = POSITION_V2.X[index] + "%";
    return `top: ${asse_y}; left: ${asse_x};`
}
