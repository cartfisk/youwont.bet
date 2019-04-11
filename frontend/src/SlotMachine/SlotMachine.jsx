import React from 'react';
import ImageUpload from '../ImageUpload/ImageUpload';
import './styles.css';

function RepeatButton(props) {
    return (
        <ImageUpload
            id='repeatButton'
            onClick={props.onClick}
        />
    );
}

export class SlotMachine extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            winner: null
        }
        this.finishHandler = this.finishHandler.bind(this)
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick() {
        this.setState({ winner: null });
        this.emptyArray();
        this._child1.forceUpdateHandler();
        this._child2.forceUpdateHandler();
        this._child3.forceUpdateHandler();
    }

    static matches = [];

    finishHandler(value) {
        SlotMachine.matches.push(value);

        if (SlotMachine.matches.length === 3) {
            const first = SlotMachine.matches[0];
            let results = SlotMachine.matches.every(match => match === first)
            this.setState({ winner: results });
        }
    }

    emptyArray() {
        SlotMachine.matches = [];
    }

    render() {
        const { winner } = this.state;
        let repeatButton = null;

        if (winner !== null) {
            repeatButton = <RepeatButton onClick={this.handleClick} />
        }

        return (
            <div className={'slot-machine-container'}>
                <div className={'spinner-container'}>
                    <Spinner onFinish={this.finishHandler} ref={(child) => { this._child1 = child; }} timer="1000" />
                    <Spinner onFinish={this.finishHandler} ref={(child) => { this._child2 = child; }} timer="1400" />
                    <Spinner onFinish={this.finishHandler} ref={(child) => { this._child3 = child; }} timer="2200" />
                    <div className="gradient-fade"></div>
                </div>
                {repeatButton}
            </div>
        );
    }
}

class Spinner extends React.Component {
    constructor(props) {
        super(props);
        this.forceUpdateHandler = this.forceUpdateHandler.bind(this);
    };

    forceUpdateHandler() {
        this.reset();
    };

    reset() {
        if (this.timer) {
            clearInterval(this.timer);
        }

        this.start = this.setStartPosition();

        this.setState({
            position: this.start,
            timeRemaining: this.props.timer
        });

        this.timer = setInterval(() => {
            this.tick()
        }, 100);
    }

    state = {
        position: 0,
        lastPosition: null
    }
    static iconHeight = 188;
    multiplier = Math.floor(Math.random() * (4 - 1) + 1);

    start = this.setStartPosition();
    speed = Spinner.iconHeight * this.multiplier;

    setStartPosition() {
        return -0;
    }

    moveBackground() {
        const position = ((this.state.position - this.speed) / 1692) * 1000;
        this.setState({
            position: position,
            timeRemaining: this.state.timeRemaining - 100
        })
    }

    getSymbolFromPosition() {
        const totalSymbols = 9;
        const maxPosition = (Spinner.iconHeight * (totalSymbols - 1) * -1);
        let moved = (this.props.timer / 100) * this.multiplier
        let startPosition = this.start;
        let currentPosition = startPosition;

        for (let i = 0; i < moved; i++) {
            currentPosition -= Spinner.iconHeight;

            if (currentPosition < maxPosition) {
                currentPosition = 0;
            }
        }

        this.props.onFinish(currentPosition);
    }

    tick() {
        if (this.state.timeRemaining <= 0) {
            clearInterval(this.timer);
            this.getSymbolFromPosition();

        } else {
            this.moveBackground();
        }
    }

    componentDidMount() {
        clearInterval(this.timer);

        this.setState({
            position: this.start,
            timeRemaining: this.props.timer
        });

        this.timer = setInterval(() => {
            this.tick()
        }, 100);
    }

    render() {
        let { position } = this.state;
        return (
            <div
                style={{ backgroundPosition: `0% ${position}%` }}
                className={`icons`}
            />
        )
    }
}